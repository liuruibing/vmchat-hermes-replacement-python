from __future__ import annotations

import json
import os
import sqlite3
import threading
import time
from pathlib import Path
from typing import Optional

from app.session.models import SessionState


class SqliteSessionStore:
    """Small persistent session store.

    The store keeps complete conversation state out of model prompts. Context
    selection happens later in SessionManager/ContextManager.
    """

    def __init__(self, path: str = ".runtime/ai-sessions.sqlite3") -> None:
        self.path = path
        if path != ":memory:":
            Path(path).expanduser().parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()
        self._conn = sqlite3.connect(path, check_same_thread=False)
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                payload_json TEXT NOT NULL,
                updated_at REAL NOT NULL
            )
            """
        )
        self._conn.commit()

    def get(self, session_id: str) -> Optional[SessionState]:
        with self._lock:
            row = self._conn.execute(
                "SELECT payload_json FROM sessions WHERE session_id = ?",
                (session_id,),
            ).fetchone()
        if not row:
            return None
        try:
            return SessionState.model_validate(json.loads(row[0]))
        except Exception:
            return None

    def put(self, state: SessionState) -> SessionState:
        payload = state.model_dump(by_alias=True)
        payload_json = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
        with self._lock:
            self._conn.execute(
                """
                INSERT INTO sessions(session_id, payload_json, updated_at)
                VALUES (?, ?, ?)
                ON CONFLICT(session_id) DO UPDATE SET
                    payload_json = excluded.payload_json,
                    updated_at = excluded.updated_at
                """,
                (state.sessionId, payload_json, state.updatedAt),
            )
            self._conn.commit()
        return state

    def delete(self, session_id: str) -> bool:
        with self._lock:
            cur = self._conn.execute(
                "DELETE FROM sessions WHERE session_id = ?",
                (session_id,),
            )
            self._conn.commit()
            return cur.rowcount > 0

    def close(self) -> None:
        with self._lock:
            self._conn.close()
