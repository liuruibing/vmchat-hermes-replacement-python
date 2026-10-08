# ==============================================================================
# 文件：app/workflow/langgraph_adapter.py
# 文件作用：提供可选的通用桥接类，让图构建与事件转换满足框架的 stream(context) 接口。
# 全局位置：需要通用桥接时，Engine → LangGraphWorkflow → 图工厂回调 → 事件适配回调。
# 谁调用它：选择使用此桥接类的扩展工作流；当前默认图流程各自实现 stream，没有经过本类。
# 输入：工作流 id、构建图的函数、转换事件的函数，以及本次 WorkflowContext。
# 输出：事件适配函数产生的异步业务事件生成器。
# 主要流程：保存两个回调 → 按 context 构建图 → 把图和 context 交给事件适配函数。
# 前端类比：像通用 adapter，将第三方组件的接口接到应用统一的 handler 约定。
# 边界：本类不是默认图流程的父类；如何执行图、如何转换事件由传入的回调决定。
# 阅读入口：先看构造参数，再看 stream()；require_langgraph() 单独检查依赖是否可用。
# ==============================================================================

from __future__ import annotations

from typing import Any, AsyncGenerator, Callable

from app.workflow.engine import WorkflowContext


class LangGraphWorkflow:
    """Optional bridge for a compiled LangGraph workflow.

    LangGraph stays behind WorkflowProtocol so the rest of the AI Runtime is not
    coupled to one workflow implementation technology.
    """

    def __init__(
        self,
        workflow_id: str,
        graph_factory: Callable[[WorkflowContext], Any],
        event_adapter: Callable[[Any, WorkflowContext], AsyncGenerator[Any, None]],
    ) -> None:
        self.id = workflow_id
        # 保存函数本身，类似把 createGraph 和 mapEvents 两个回调传入 JS 类的构造函数。
        self._graph_factory = graph_factory
        self._event_adapter = event_adapter

    def stream(self, context: WorkflowContext) -> AsyncGenerator[Any, None]:
        # 先用本次上下文构建图，再由事件适配函数决定如何执行图、转换业务事件。
        graph = self._graph_factory(context)
        return self._event_adapter(graph, context)


def require_langgraph() -> Any:
    # 延迟导入：只有调用这个检查入口时才确认依赖是否可用，并给出可读的异常。
    try:
        import langgraph  # type: ignore
    except ImportError as err:
        raise RuntimeError(
            "LANGGRAPH_NOT_INSTALLED: install LangGraph before registering a "
            "LangGraph-backed workflow"
        ) from err
    return langgraph
