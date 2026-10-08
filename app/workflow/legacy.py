# ==============================================================================
# 文件：app/workflow/legacy.py
# 文件作用：建立默认工作流目录，同时保留旧函数式流程的包装接口。
# 全局位置：main.py → build_default_workflow_registry() → WorkflowRegistry → WorkflowEngine。
# 谁调用它：main.py 启动时调用默认注册函数；旧包装类供需要兼容旧调用方式的代码使用。
# 输入：旧流程函数参数；默认注册函数目前创建的是下面导入的工作流实例。
# 输出：包含 simple-chat、vm-report、mandate-risk-analysis 和 mandate-risk-analysis-v2 的目录。
# 主要流程：导入各流程实现 → 创建实例 → 交给 WorkflowRegistry 登记各自的 id。
# 前端类比：像 routes.js / 插件注册清单，告诉应用哪些功能由哪些实现处理。
# 边界：文件名虽叫 legacy，这里仍是默认注册入口；前三个流程用 LangGraph，V2 直接用 Python。
# 阅读入口：先看文件末尾的 build_default_workflow_registry()，再按类名跳到 graphs/ 中。
# ==============================================================================

from __future__ import annotations

from typing import Any, AsyncGenerator, Callable

from app.contracts.types import VmChatRunError
from app.workflow.engine import WorkflowContext


class SimpleChatWorkflow:
    id = "simple-chat"

    def __init__(self, stream_fn: Callable[..., AsyncGenerator[Any, None]]) -> None:
        self._stream_fn = stream_fn

    def stream(self, context: WorkflowContext) -> AsyncGenerator[Any, None]:
        # 适配旧接口：将一个 context 对象拆成旧函数需要的命名参数。
        return self._stream_fn(
            input_val=context.input_val,
            provider=context.provider,
            skill_md=context.skill_md,
            role_prompt=context.role_prompt,
            knowledge_search=context.knowledge_search,
            signal=context.signal,
            message_chunk_chars=context.message_chunk_chars,
        )


class VmReportWorkflow:
    id = "vm-report"

    def __init__(self, stream_fn: Callable[..., AsyncGenerator[Any, None]]) -> None:
        self._stream_fn = stream_fn

    def stream(self, context: WorkflowContext) -> AsyncGenerator[Any, None]:
        if context.resources is None:
            raise VmChatRunError(
                "SERVICE_DEGRADED",
                "当前 Agent 资源尚未加载完成",
            )
        return self._stream_fn(
            {
                "input": context.input_val,
                "resources": context.resources,
                "provider": context.provider,
                "signal": context.signal,
                "message_chunk_chars": context.message_chunk_chars,
                "role_prompt": context.role_prompt,
                "knowledge_search": context.knowledge_search,
            }
        )


def build_default_workflow_registry(
    *,
    simple_chat_stream: Callable[..., AsyncGenerator[Any, None]],
    vm_report_stream: Callable[..., AsyncGenerator[Any, None]],
):
    # simple_chat_stream / vm_report_stream 参数保留接口兼容；下面的默认列表没有使用它们。
    from app.workflow.registry import WorkflowRegistry

    from app.workflow.graphs.mandate_risk import MandateRiskLangGraphWorkflow
    from app.workflow.graphs.mandate_risk_v2 import MandateRiskV2Workflow
    from app.workflow.graphs.performance_report import PerformanceReportLangGraphWorkflow
    from app.workflow.graphs.simple_chat import SimpleChatLangGraphWorkflow

    # V2 is registered under a separate workflow id only. Existing agents stay
    # on mandate-risk-analysis until the V2 accuracy gates are proven on real
    # PDFs; registering it here merely makes explicit lab invocation possible.
    # 注册是建立 id → 实例的映射，不会立即调用模型或执行任何流程。
    # simple-chat / vm-report / mandate-risk-analysis 使用 LangGraph；V2 是普通 Python 异步流程。
    return WorkflowRegistry(
        [
            SimpleChatLangGraphWorkflow(),
            PerformanceReportLangGraphWorkflow(),
            MandateRiskLangGraphWorkflow(),
            MandateRiskV2Workflow(),
        ]
    )
