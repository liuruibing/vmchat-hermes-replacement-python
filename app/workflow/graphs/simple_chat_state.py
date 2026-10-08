# ==============================================================================
# 文件：app/workflow/graphs/simple_chat_state.py
# 文件作用：定义普通聊天图在节点之间传递的数据结构。
# 全局位置：simple_chat.py 的初始输入 → retrieve_knowledge/answer 更新 → 最终图结果。
# 谁调用它：simple_chat.py 将此类型传给 StateGraph，并用于声明初始状态和节点输入。
# 输入：本次用户问题、摘要、历史消息；节点随后补充检索资料、答案、过程说明和用量。
# 输出：类型约定；本文件本身不生成答案，也不创建运行中的状态对象。
# 主要流程：user_message/history → knowledge_context → answer/reasoning/usage；error 传递失败信息。
# 前端类比：像为一次分析任务的 store 定义 TypeScript interface。
# 边界：TypedDict 不做运行时校验；没有 reducer，同名字段更新时覆盖旧值，列表不自动追加。
# 阅读入口：先看 SimpleChatGraphState 字段，再对照 simple_chat.py 中节点 return 的字典。
# ==============================================================================

from __future__ import annotations

from typing import Any, Dict, List, TypedDict


# TypedDict 类似 TS interface，只描述字典形状，不像 Pydantic 那样做运行时校验。
# total=False 表示字段可以缺省；节点只返回自己更新的字段，LangGraph 把更新写入 state。
# 这些字段没声明 reducer（合并函数），所以再次返回同名字段时会覆盖原值，列表也不会自动追加。
class SimpleChatGraphState(TypedDict, total=False):
    user_message: str  # 本次问题。
    session_summary: str  # 上层 Context 服务提供的会话摘要。
    history: List[Dict[str, str]]  # 历史消息，每项包含 role / content。
    knowledge_context: str  # retrieve_knowledge 节点检索到的资料。
    answer: str  # answer 节点拼好的完整答案。
    reasoning: List[str]  # 收集的过程说明片段。
    usage: Dict[str, Any]  # 模型报告的 token 用量。
    error: str  # 非空时停止有效业务处理，最终转成失败事件。
