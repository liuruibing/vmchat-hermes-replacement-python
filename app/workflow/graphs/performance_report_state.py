# ==============================================================================
# 文件：app/workflow/graphs/performance_report_state.py
# 文件作用：定义报表图的任务状态，把生成、校验和修复所需的数据串起来。
# 全局位置：performance_report.py 初始状态 → 各节点更新 → 最终文字或 DSL 结果。
# 谁调用它：performance_report.py 将此类型传给 StateGraph，并作为各节点的输入类型。
# 输入：指标语义计划、模型候选、校验问题、读取资源记录和尝试次数等中间数据。
# 输出：字段及类型的约定；不是实际执行校验、修复或保存数据库的模块。
# 主要流程：resolved_metrics → raw_output/candidate → validation_errors/validated_dsls → final_text。
# 前端类比：像多步表单的 TS state 类型，把草稿、错误、提交状态和重试计数放在一起。
# 边界：TypedDict 只作类型提示；节点返回同名字段会覆盖，累计用量由节点自己读取再相加。
# 阅读入口：先看 candidate、validation_ok、candidate_dirty、repair_attempts，再对照图的分支。
# ==============================================================================

from __future__ import annotations

from typing import Any, Dict, List, TypedDict


# 可以把 state 理解为本次报表任务的 store；它不是整个应用的全局 store。
# TypedDict 只做类型提示；total=False 允许部分字段暂时不存在，节点返回局部更新。
# 未定义 reducer，所以同名字段会覆盖；修复节点先读取旧 usage，再累加并返回新字典。
class PerformanceReportGraphState(TypedDict, total=False):
    resolved_metrics: List[Dict[str, Any]]
    semantic_plan: Dict[str, Any]
    raw_output: str  # 模型的原始回答，还没通过报表业务校验。
    candidate: Any  # 从回答中解析出的待校验 DSL（报表 JSON 配置）。
    validation_errors: List[Dict[str, Any]]  # 校验问题，修复时作为反馈交给模型。
    validated_dsls: List[Any]  # 校验器认可的报表配置。
    validation_ok: bool  # 路由函数据此选择输出或修复。
    candidate_dirty: bool  # 候选内容已更新、需要重校验；不是前端页面的未保存标记。
    result_type: str
    final_text: str
    reasoning: List[str]
    usage: Dict[str, int]
    read_resource_paths: List[str]  # 生成时读取的资源，修复时可以复用相同上下文。
    attempt_count: int  # 首次生成和修复的总尝试次数。
    repair_attempts: int  # 只计修复次数，用来控制循环上限。
    error_code: str
    error_message: str
