from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Sequence

from app.compatibility.hermes_request import CurrentDslItem, VmChatInput, VmReportDsl
from app.session.models import SessionState
from app.session.manager import SessionManager


def _estimate_tokens(text: str) -> int:
    """Conservative tokenizer-free estimate suitable for mixed Chinese/JSON text."""
    if not text:
        return 0
    ascii_chars = sum(1 for ch in text if ord(ch) < 128)
    non_ascii = len(text) - ascii_chars
    return int(ascii_chars / 3.6 + non_ascii / 1.35) + 1


def _query_terms(text: str) -> set[str]:
    source = str(text or "").lower()
    terms = set(re.findall(r"[a-z0-9_]{2,}|[\u3400-\u9fff]{2,}", source))
    for phrase in list(terms):
        if re.fullmatch(r"[\u3400-\u9fff]{4,}", phrase):
            for size in (2, 3, 4):
                for idx in range(max(0, len(phrase) - size + 1)):
                    terms.add(phrase[idx:idx + size])
    return terms


@dataclass
class ContextBudgetReport:
    history_tokens: int = 0
    dsl_tokens: int = 0
    summary_tokens: int = 0
    total_estimated_tokens: int = 0
    full_dsl_blocks: int = 0
    summarized_dsl_blocks: int = 0


class ContextManager:
    """Builds bounded model context from durable server-side session state.

    Frontend state remains authoritative for the current page, but the frontend
    no longer decides how much conversation history or which full DSL blocks the
    model receives.
    """

    def __init__(
        self,
        session_manager: SessionManager,
        max_context_tokens: int = 32000,
        max_dsl_tokens: int = 9000,
        max_history_tokens: int = 5000,
    ) -> None:
        self.session_manager = session_manager
        self.max_context_tokens = max(8000, max_context_tokens)
        self.max_dsl_tokens = max(2000, max_dsl_tokens)
        self.max_history_tokens = max(1000, max_history_tokens)

    def _dsl_dict(self, item: CurrentDslItem) -> Dict[str, Any]:
        value = item.dsl.model_dump(exclude_none=True) if hasattr(item.dsl, "model_dump") else item.dsl
        return dict(value) if isinstance(value, dict) else {}

    def _summary_dsl(self, item: CurrentDslItem) -> Dict[str, Any]:
        dsl = self._dsl_dict(item)
        requests = []
        for request in dsl.get("requests") or []:
            if hasattr(request, "model_dump"):
                request = request.model_dump(exclude_none=True)
            if not isinstance(request, dict):
                continue
            requests.append(
                {
                    key: request.get(key)
                    for key in ("id", "moduleId", "submoduleId", "sqlCode")
                    if request.get(key) not in (None, "")
                }
            )

        view = dsl.get("view") if isinstance(dsl.get("view"), dict) else {}
        columns = []
        for column in view.get("columns") or []:
            if isinstance(column, dict):
                compact = {
                    key: column.get(key)
                    for key in ("field", "label", "unit")
                    if column.get(key) not in (None, "")
                }
                if compact:
                    columns.append(compact)
        series = []
        for item_series in view.get("series") or []:
            if isinstance(item_series, dict):
                compact = {
                    key: item_series.get(key)
                    for key in ("name", "type", "encode")
                    if item_series.get(key) not in (None, "")
                }
                if compact:
                    series.append(compact)

        compact_view = {
            key: view.get(key)
            for key in ("type", "title")
            if view.get(key) not in (None, "")
        }
        if columns:
            compact_view["columns"] = columns[:20]
        if series:
            compact_view["series"] = series[:20]

        return {
            "action": dsl.get("action"),
            "id": dsl.get("id") or item.id,
            "title": dsl.get("title") or item.title,
            "requests": requests,
            "view": compact_view,
        }

    def _block_relevance(self, item: CurrentDslItem, query_terms: set[str]) -> float:
        haystack = f"{item.title} {item.viewType or ''}".lower()
        dsl = self._dsl_dict(item)
        for request in dsl.get("requests") or []:
            if hasattr(request, "model_dump"):
                request = request.model_dump(exclude_none=True)
            if isinstance(request, dict):
                haystack += " " + " ".join(
                    str(request.get(key) or "")
                    for key in ("moduleId", "submoduleId", "sqlCode")
                )
        view = dsl.get("view") if isinstance(dsl.get("view"), dict) else {}
        haystack += " " + str(view.get("title") or "")
        for column in view.get("columns") or []:
            if isinstance(column, dict):
                haystack += " " + " ".join(
                    str(column.get(key) or "")
                    for key in ("field", "label", "unit")
                )
        for series in view.get("series") or []:
            if isinstance(series, dict):
                haystack += " " + " ".join(
                    str(series.get(key) or "")
                    for key in ("name", "type")
                )
        block_terms = _query_terms(haystack)
        return float(len(query_terms.intersection(block_terms)))

    def compact_dsls(
        self,
        current_dsls: Sequence[CurrentDslItem],
        selected_block_id: str | None,
        user_message: str,
    ) -> tuple[List[CurrentDslItem], int, int]:
        if not current_dsls:
            return [], 0, 0

        query_terms = _query_terms(user_message)
        full_ids: set[str] = set()
        if selected_block_id:
            full_ids.add(selected_block_id)

        ranked = sorted(
            current_dsls,
            key=lambda item: self._block_relevance(item, query_terms),
            reverse=True,
        )
        for item in ranked:
            if len(full_ids) >= 3:
                break
            if self._block_relevance(item, query_terms) > 0:
                full_ids.add(item.blockId)

        # Small pages are cheap enough to keep complete and avoid accidental
        # loss of cross-block references.
        if len(current_dsls) <= 3:
            full_ids.update(item.blockId for item in current_dsls)

        result: List[CurrentDslItem] = []
        full_count = 0
        summary_count = 0

        for item in current_dsls:
            if item.blockId in full_ids:
                result.append(item)
                full_count += 1
            else:
                result.append(
                    CurrentDslItem(
                        blockId=item.blockId,
                        id=item.id,
                        title=item.title,
                        viewType=item.viewType,
                        dsl=self._summary_dsl(item),
                    )
                )
                summary_count += 1

        def serialized_tokens(values: Sequence[CurrentDslItem]) -> int:
            payload = [
                value.model_dump(exclude_none=True)
                for value in values
            ]
            return _estimate_tokens(json.dumps(payload, ensure_ascii=False))

        # If even selected/relevant full blocks are too large, progressively
        # downgrade non-selected full blocks to summaries.
        while serialized_tokens(result) > self.max_dsl_tokens:
            downgrade_index = next(
                (
                    idx for idx in range(len(result) - 1, -1, -1)
                    if result[idx].blockId != selected_block_id
                    and result[idx].blockId in full_ids
                ),
                None,
            )
            if downgrade_index is None:
                break
            original = current_dsls[downgrade_index]
            result[downgrade_index] = CurrentDslItem(
                blockId=original.blockId,
                id=original.id,
                title=original.title,
                viewType=original.viewType,
                dsl=self._summary_dsl(original),
            )
            full_ids.discard(original.blockId)
            full_count = max(0, full_count - 1)
            summary_count += 1

        return result, full_count, summary_count

    def prepare(
        self,
        state: SessionState,
        incoming: VmChatInput,
    ) -> tuple[VmChatInput, ContextBudgetReport]:
        self.session_manager.bootstrap_history(state, incoming)
        history = self.session_manager.select_history(state, incoming.userMessage)

        # Hard cap history after semantic/recent selection.
        bounded_history = []
        history_tokens = 0
        for message in reversed(history):
            tokens = _estimate_tokens(message.content)
            if bounded_history and history_tokens + tokens > self.max_history_tokens:
                continue
            if tokens > self.max_history_tokens:
                content = message.content[-max(1000, int(self.max_history_tokens * 2.2)) :]
                tokens = _estimate_tokens(content)
                message = type(message)(role=message.role, content=content)
            bounded_history.append(message)
            history_tokens += tokens
        bounded_history.reverse()

        compact_dsls, full_count, summary_count = self.compact_dsls(
            incoming.currentDsls,
            incoming.selectedBlockId,
            incoming.userMessage,
        )

        summary = state.summary or ""
        summary_tokens = _estimate_tokens(summary)
        dsl_tokens = _estimate_tokens(
            json.dumps(
                [item.model_dump(exclude_none=True) for item in compact_dsls],
                ensure_ascii=False,
            )
        )

        prepared = incoming.model_copy(
            update={
                "historyMessages": bounded_history,
                "currentDsls": compact_dsls,
                "sessionSummary": summary,
                "agentId": state.agentId,
                "roleId": state.roleId,
            }
        )

        report = ContextBudgetReport(
            history_tokens=history_tokens,
            dsl_tokens=dsl_tokens,
            summary_tokens=summary_tokens,
            total_estimated_tokens=history_tokens + dsl_tokens + summary_tokens,
            full_dsl_blocks=full_count,
            summarized_dsl_blocks=summary_count,
        )
        return prepared, report
