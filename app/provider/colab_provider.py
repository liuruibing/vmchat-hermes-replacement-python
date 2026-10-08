# ==============================================================================
# 文件：app/provider/colab_provider.py
# 文件作用：让只支持文字消息的 Colab 模型入口，也能参与项目的工具调用流程。
# 全局位置：工作流 → ColabVmChatProvider → TextToolModel → LangChain 模型客户端 → Colab 服务。
# 谁调用它：main.py 在 LLM_PROVIDER=colab 时选择该 Provider；工具循环复用父类 run_skill()。
# 输入：原模型对象、工具定义，以及普通消息、模型工具请求和 Python 工具执行结果。
# 输出：统一的 AIMessageChunk；请求工具时带 tool_call_chunks，回答时带正文与用量。
# 主要流程：把工具协议写成文字 JSON → 请求模型 → 合并完整一轮 → 识别并转换工具请求。
# 前端类比：像兼容旧接口的 adapter，将服务的特殊协议转换成上层统一格式。
# 边界：它转换消息协议；实际读文件/查知识仍由父类工具循环执行，不会直接执行模型给出的代码。
# 阅读入口：先看 ColabVmChatProvider.build_model()，再看 TextToolModel.astream()。
# ==============================================================================

"""Text tool transport for Colab's built-in, text-only model proxy."""

# 阅读地图：Colab 入口仅接收文字，这个包装器把工具调用翻译成文字 JSON 协议。
# 它仍复用父类 run_skill 的工具循环，只替换模型的 bind_tools/astream 交互方式。
import json
import os
import uuid

from langchain_core.messages import AIMessageChunk, ToolMessage
from langchain_core.utils.function_calling import convert_to_openai_tool

from app.provider.langchain_provider import LangChainVmChatProvider, extract_first_json_value


# 类似前端给 API client 包一层 adapter：保留原客户端，用包装对象兼容特殊服务。
class TextToolModel:
    def __init__(self, model, tools=()):
        self.model = model
        self.tools = list(tools)

    # 包装器没有的属性/方法转交给原客户端，类似 Proxy 的属性读取代理。
    def __getattr__(self, name):
        return getattr(self.model, name)

    # 保存工具定义到新包装对象；这个入口不能直接使用服务端原生工具调用。
    def bind_tools(self, tools):
        return TextToolModel(self.model, tools)

    async def astream(self, messages):
        # 从 @tool 定义提取名称/参数/说明，把 schema 放进系统文字，告诉模型如何写调用 JSON。
        schemas = [convert_to_openai_tool(t)['function'] for t in self.tools]
        tool_names = {schema['name'] for schema in schemas}
        instruction = (
            '工具传输协议：此模型入口不支持原生工具调用。需要调用工具时，只输出一个 JSON 对象：'
            '{"colab_tool_calls":[{"name":"工具名","arguments":{"参数名":"参数值"}}]}。'
            '不要伪造工具结果。收到 TOOL_RESULT 后继续处理，可再次调用工具。'
            '不需要工具或已取得资源时，直接按原任务要求输出最终答案或 DSL，'
            '最终答案不要使用 colab_tool_calls 字段。可用工具：\n'
            + json.dumps(schemas, ensure_ascii=False)
        )
        text_messages = [{'role': 'system', 'content': instruction}]
        # 父类消息可能是字典或 LangChain 对象；统一转成该入口可接收的 role/content 文字。
        for message in messages:
            if isinstance(message, dict):
                text_messages.append(dict(message))
            # 工具结果也要转成文字；保留调用 ID，让模型知道每份结果对应哪次请求。
            elif isinstance(message, ToolMessage):
                text_messages.append({
                    'role': 'user',
                    'content': 'TOOL_RESULT ' + message.tool_call_id + '\n' + str(message.content),
                })
            # 把模型上一轮的工具请求写回 assistant 消息，保留多轮对话的来龙去脉。
            elif getattr(message, 'tool_calls', None):
                text_messages.append({
                    'role': 'assistant',
                    'content': json.dumps({'colab_tool_calls': [
                        {'name': c['name'], 'arguments': c['args'], 'id': c['id']}
                        for c in message.tool_calls
                    ]}, ensure_ascii=False),
                })
            else:
                text_messages.append({'role': 'assistant', 'content': str(message.content)})

        # 虽然底层 astream 逐块返回，这里先拼完整轮输出才能判断它是调用 JSON 还是最终答案。
        # 因而包装器不会逐 token 向外 yield；上层收到的是这一轮合并后的消息。
        response = None
        async for chunk in self.model.astream(text_messages):
            response = response + chunk if response is not None else chunk
        if response is None:
            raise RuntimeError('COLAB_MODEL_EMPTY_RESPONSE')
        # 提取/解析 JSON 只是识别传输协议；普通 DSL 或文字答案会原样交回父类。
        raw_json = extract_first_json_value(response.content) if isinstance(response.content, str) else None
        try:
            payload = json.loads(raw_json) if raw_json else None
        except json.JSONDecodeError:
            payload = None
        if not isinstance(payload, dict) or 'colab_tool_calls' not in payload:
            yield response
            return

        # 模型生成的调用需要校验数量、工具名及参数对象，不能因为它来自模型就直接执行。
        calls = payload['colab_tool_calls']
        if not isinstance(calls, list) or not 1 <= len(calls) <= 8:
            raise RuntimeError('COLAB_TOOL_REQUEST_INVALID: expected 1 to 8 tool calls')
        chunks = []
        for index, call in enumerate(calls):
            if (not isinstance(call, dict) or call.get('name') not in tool_names
                    or not isinstance(call.get('arguments'), dict)):
                raise RuntimeError('COLAB_TOOL_REQUEST_INVALID: unknown tool or invalid arguments')
            chunks.append({
                'name': call['name'], 'args': json.dumps(call['arguments'], ensure_ascii=False),
                'id': 'colab_' + uuid.uuid4().hex, 'index': index,
            })
        # 将文字 JSON 转成 LangChain 工具片段。这里只转换格式，实际工具执行仍在父类 run_skill。
        # 随机 ID 用于 ToolMessage 关联结果；保留底层用量供父类汇总。
        yield AIMessageChunk(content='', tool_call_chunks=chunks, usage_metadata=response.usage_metadata)


# 继承让 generate/stream/run_skill 沿用父类，只覆盖客户端构建，插入文本工具协议包装。
class ColabVmChatProvider(LangChainVmChatProvider):
    def build_model(self, *, timeout_seconds=120):
        # super() 调用父类：先用原有配置/路由创建客户端，再设置 Colab 输出上限并包一层。
        model = super().build_model(timeout_seconds=timeout_seconds)
        model.max_tokens = int(os.getenv('COLAB_MAX_OUTPUT_TOKENS', '16384'))
        return TextToolModel(model)
