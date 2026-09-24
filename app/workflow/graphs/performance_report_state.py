from __future__ import annotations

from typing import Any, Dict, List, TypedDict


class PerformanceReportGraphState(TypedDict, total=False):
    resolved_metrics: List[Dict[str, Any]]
    semantic_plan: Dict[str, Any]
    raw_output: str
    candidate: Any
    validation_errors: List[Dict[str, Any]]
    validated_dsls: List[Any]
    validation_ok: bool
    candidate_dirty: bool
    result_type: str
    final_text: str
    reasoning: List[str]
    usage: Dict[str, int]
    read_resource_paths: List[str]
    attempt_count: int
    repair_attempts: int
    error_code: str
    error_message: str
