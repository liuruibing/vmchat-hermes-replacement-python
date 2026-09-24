from __future__ import annotations

from typing import Any, Dict, List, TypedDict


class SimpleChatGraphState(TypedDict, total=False):
    user_message: str
    session_summary: str
    history: List[Dict[str, str]]
    knowledge_context: str
    answer: str
    reasoning: List[str]
    usage: Dict[str, Any]
    error: str
