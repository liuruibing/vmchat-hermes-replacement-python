from __future__ import annotations

import json
import math
import re
import time
from typing import Iterable, List, Optional

from app.compatibility.hermes_request import HermesChatMessage, VmChatInput
from app.session.models import SessionMessage, SessionState, SessionUiState
from app.session.store import SqliteSessionStore


def _terms(text: str) -> set[str]:
    source = str(text or "").lower()
    words = set(re.findall(r"[a-z0-9_]{2,}|[\u3400-\u9fff]{2,}", source))
    # Chinese phrases often contain several concepts without spaces. Small
    # character n-grams make old-message retrieval useful without a tokenizer.
    for phrase in list(words):
        if re.fullmatch(r"[\u3400-\u9fff]{4,}", phrase):
            for size in (2, 3, 4):
                for i in range(0, max(0, len(phrase) - size + 1)):
                    words.add(phrase[i:i + size])
    return words


class SessionManager:
    def __init__(
        self,
        store: SqliteSessionStore,
        recent_messages: int = 6,
        relevant_history_messages: int = 4,
        max_messages_per_session: int = 400,
    ) -> None:
        self.store = store
        self.recent_messages = max(2, recent_messages)
        self.relevant_history_messages = max(0, relevant_history_messages)
        self.max_messages_per_session = max(20, max_messages_per_session)

    def get_or_create(
        self,
        session_id: str,
        agent_id: str = "performance-ai",
        role_id: str = "performance-analyst",
    ) -> SessionState:
        now = time.time()
        existing = self.store.get(session_id)
        if existing is not None:
            if agent_id:
                existing.agentId = agent_id
            if role_id:
                existing.roleId = role_id
            existing.updatedAt = now
            return existing
        state = SessionState(
            session_id=session_id,
            agent_id=agent_id,
            role_id=role_id,
            created_at=now,
            updated_at=now,
        )
        self.store.put(state)
        return state

    def bootstrap_history(self, state: SessionState, incoming: VmChatInput) -> None:
        # Compatibility path for old frontends. Only seed an empty server-side
        # session; once Python owns the session, frontend history is ignored.
        if state.messages or not incoming.historyMessages:
            return
        now = time.time()
        for item in incoming.historyMessages[-20:]:
            state.messages.append(
                SessionMessage(
                    role=item.role,
                    content=item.content[:16000],
                    created_at=now,
                )
            )
        state.updatedAt = now
        self.store.put(state)

    def select_history(self, state: SessionState, query: str) -> List[HermesChatMessage]:
        messages = state.messages
        if not messages:
            return []

        recent_start = max(0, len(messages) - self.recent_messages)
        selected_indexes = set(range(recent_start, len(messages)))

        if self.relevant_history_messages > 0 and recent_start > 0:
            query_terms = _terms(query)
            scored: list[tuple[float, int]] = []
            for index, message in enumerate(messages[:recent_start]):
                msg_terms = _terms(message.content)
                overlap = len(query_terms.intersection(msg_terms))
                if overlap <= 0:
                    continue
                recency = (index + 1) / max(1, recent_start)
                score = overlap + 0.15 * recency
                scored.append((score, index))
            scored.sort(reverse=True)
            for _, index in scored[: self.relevant_history_messages]:
                selected_indexes.add(index)

        return [
            HermesChatMessage(role=messages[index].role, content=messages[index].content)
            for index in sorted(selected_indexes)
        ]

    def update_ui_state(self, state: SessionState, incoming: VmChatInput) -> None:
        summaries = []
        for item in incoming.currentDsls:
            dsl = item.dsl.model_dump(exclude_none=True) if hasattr(item.dsl, "model_dump") else item.dsl
            if not isinstance(dsl, dict):
                dsl = {}
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
            summaries.append(
                {
                    "blockId": item.blockId,
                    "id": item.id,
                    "title": item.title,
                    "viewType": item.viewType or view.get("type"),
                    "requests": requests,
                }
            )

        state.uiState = SessionUiState(
            selected_block_id=incoming.selectedBlockId,
            global_query_parameters={
                "names": list(incoming.globalQueryParameters.names),
                "nonemptyFlags": dict(incoming.globalQueryParameters.nonemptyFlags),
            },
            block_summaries=summaries,
        )
        state.updatedAt = time.time()
        self.store.put(state)

    def _refresh_summary(self, state: SessionState) -> None:
        # Keep the durable full history in SQLite, but give the model a bounded
        # synopsis of older turns. This deterministic summarizer is deliberately
        # replaceable by an LLM summarizer later.
        if len(state.messages) <= 16:
            return
        older = state.messages[:-10]
        lines: List[str] = []
        for message in older[-24:]:
            clean = " ".join(str(message.content or "").split())
            if not clean:
                continue
            if clean.startswith("[artifact:"):
                clean = clean[:260]
            else:
                clean = clean[:220]
            prefix = "用户" if message.role == "user" else "助手"
            lines.append(f"{prefix}: {clean}")
        if lines:
            state.summary = ("较早会话要点：\n" + "\n".join(lines))[-4000:]

    def complete_turn(
        self,
        state: SessionState,
        user_message: str,
        assistant_output: str,
        run_id: Optional[str] = None,
        artifact_id: Optional[str] = None,
    ) -> SessionState:
        now = time.time()
        state.messages.extend(
            [
                SessionMessage(
                    role="user",
                    content=str(user_message or "")[:16000],
                    created_at=now,
                    run_id=run_id,
                ),
                SessionMessage(
                    role="assistant",
                    content=(
                        f"[artifact:{artifact_id}] 已生成或更新结构化报表结果。"
                        if artifact_id
                        else str(assistant_output or "")[:12000]
                    ),
                    created_at=now,
                    run_id=run_id,
                ),
            ]
        )
        if len(state.messages) > self.max_messages_per_session:
            state.messages = state.messages[-self.max_messages_per_session :]
        if artifact_id and artifact_id not in state.artifactIds:
            state.artifactIds.append(artifact_id)
            state.artifactIds = state.artifactIds[-100:]
        self._refresh_summary(state)
        state.updatedAt = now
        self.store.put(state)
        return state

    def delete(self, session_id: str) -> bool:
        return self.store.delete(session_id)
