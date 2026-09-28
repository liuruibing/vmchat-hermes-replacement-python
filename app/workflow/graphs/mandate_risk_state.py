from __future__ import annotations

from typing import Any, Dict, List, TypedDict


class MandateRiskGraphState(TypedDict, total=False):
    document_name: str
    document_text: str
    strategy_type: str
    strategy_confidence: float
    candidate_row_ids: List[int]
    candidates: List[Dict[str, Any]]
    model_payload: Dict[str, Any]
    result: Dict[str, Any]
    markdown: str
    reasoning: List[str]
    usage: Dict[str, int]
    error: str
