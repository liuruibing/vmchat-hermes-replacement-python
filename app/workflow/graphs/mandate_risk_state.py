# ==============================================================================
# 文件：app/workflow/graphs/mandate_risk_state.py
# 文件作用：定义 V1 风险分析图各阶段共享的数据结构。
# 全局位置：mandate_risk.py 初始文档 → 召回/审计/判断/校验节点 → 报告输出。
# 谁调用它：mandate_risk.py 将此类型传给 StateGraph，并用于声明节点输入和初始状态。
# 输入：文档文字、策略类型、候选指标、覆盖审计记录、模型答案和用量等数据。
# 输出：状态字段的类型约定；本文件不读取 PDF、不请求模型、不计算业务匹配结果。
# 主要流程：document_text → candidates → model_payload → result → markdown。
# 前端类比：像接口数据到页面 view model 之间的 TS store 类型。
# 边界：TypedDict 不自动校验字段；节点自行校验数据，同名字段返回时覆盖原值。
# 阅读入口：先看 candidate_row_ids、model_payload、result、markdown，再对照各节点 return。
# ==============================================================================

from __future__ import annotations

from typing import Any, Dict, List, TypedDict


# V1 风险分析的任务数据：文档 → 候选指标 → 模型判断 → 校验结果 → Markdown。
# TypedDict 类似 TS interface，不做运行时校验；total=False 允许节点只提交部分字段。
# 这里没有 reducer，所以节点提交同名列表时会覆盖旧列表，不会自动拼接。
class MandateRiskGraphState(TypedDict, total=False):
    document_name: str
    document_text: str
    strategy_type: str
    strategy_confidence: float
    candidate_row_ids: List[int]  # 本次送模型审核的真实指标库行号。
    candidates: List[Dict[str, Any]]  # 候选指标与条款提示，用字典保存以便图状态记录。
    coverage_audit_row_ids: List[int]  # 覆盖审计新增召回的行号，用于后续匹配级别保护。
    coverage_audit_calls: int  # 审计调用次数，与 usage 报告数量对比，判断统计是否完整。
    coverage_audit_usage_reports: List[Dict[str, int]]
    coverage_audit_reasoning: List[str]
    model_payload: Dict[str, Any]  # 已解析 JSON、但尚未完成业务校验的模型答案。
    result: Dict[str, Any]  # Python 业务校验器生成的结果。
    markdown: str  # 最终可展示的报告文本。
    reasoning: List[str]
    usage: Dict[str, int]
    error: str
