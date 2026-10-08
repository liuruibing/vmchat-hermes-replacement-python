# ==============================================================================
# 文件：app/workflow/engine.py
# 文件作用：定义工作流共同的输入/接口，并按 workflow id 分发本次任务。
# 全局位置：main.py → WorkflowEngine.stream() → registry.require(id) → 具体工作流.stream(context)。
# 谁调用它：main.py 组装 WorkflowContext 并调用 Engine；具体流程使用这里定义的接口约定。
# 输入：工作流 id 和 WorkflowContext，包含问题、Provider、资料读取回调与取消信号等。
# 输出：具体流程返回的异步业务事件生成器，由 main.py 消费后转成 SSE。
# 主要流程：WorkflowContext 装参数 → WorkflowProtocol 约定接口 → WorkflowEngine 找实例并转交执行。
# 前端类比：context 像 props + 回调；Protocol 像 TS interface；Engine 像按名称选 handler 的分发器。
# 边界：Engine 不选模型、不调度图节点；工作流内部可以用 LangGraph，也可以直接写 Python。
# 阅读入口：先看 WorkflowContext，再看 WorkflowProtocol，最后看 WorkflowEngine.stream()。
# ==============================================================================

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, AsyncGenerator, Callable, List, Optional, Protocol, runtime_checkable

from app.compatibility.hermes_request import VmChatInput


# @dataclass 自动生成构造方法，调用 WorkflowContext(input_val=..., provider=...) 就能装入数据。
# 可以把它理解为带构造方法的 TypeScript interface；类型提示本身不会自动校验传入值。
@dataclass
class WorkflowContext:
    """Runtime inputs shared by every Agent workflow.

    Long-lived conversation/knowledge/artifact state stays in the AI Runtime.
    A workflow only receives the bounded, current-run context it needs.
    Uploaded document bodies are resolved lazily by document id so they are not
    copied into chat history or generic run prompts.
    """

    input_val: VmChatInput  # 已规范化的请求，包含用户问题、历史消息和当前报表等。
    provider: Any  # 模型调用接口；流程不必知道底层是 LangChain、OMP 还是测试实现。
    agent_id: str
    role_id: str
    role_prompt: str = ""
    skill_md: str = ""
    # Callable 类似 TS 的 (query: string) => string；None 表示本次没有提供检索能力。
    knowledge_search: Optional[Callable[[str], str]] = None
    resources: Any = None
    signal: Optional[Any] = None  # 类似前端 AbortController 的取消信号，节点和 Provider 都会检查。
    message_chunk_chars: int = 256
    run_id: Optional[str] = None
    session_id: Optional[str] = None
    # 每次创建 context 都生成自己的空列表，避免不同任务共享同一个可变列表。
    document_ids: List[str] = field(default_factory=list)
    document_loader: Optional[Callable[[str], Any]] = None  # 按 id 读取已解析的 PDF，按需加载。


# Protocol 类似 TS interface：约定对象有 id 和 stream()，不同类可以实现同一约定。
# @runtime_checkable 允许用 isinstance 做结构检查，但不负责校验参数类型。
@runtime_checkable
class WorkflowProtocol(Protocol):
    id: str

    def stream(self, context: WorkflowContext) -> AsyncGenerator[Any, None]:
        # AsyncGenerator 可以用 async for 逐个读取；yield 的是业务事件，不一定是模型 token。
        ...


class WorkflowEngine:
    """Dispatch a named workflow without coupling the runtime to LangGraph."""

    def __init__(self, registry: Any) -> None:
        self.registry = registry

    def stream(
        self,
        workflow_id: str,
        context: WorkflowContext,
    ) -> AsyncGenerator[Any, None]:
        # registry 类似按 key 保存实例的 Map；require 找不到时会抛错，不会悄悄换流程。
        workflow = self.registry.require(workflow_id)
        # 返回事件生成器，由 main.py 消费并转成 SSE；这里不执行模型选择或图节点调度。
        return workflow.stream(context)
