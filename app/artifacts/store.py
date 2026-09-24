from __future__ import annotations

import json
import sqlite3
import threading
import time
import uuid
from pathlib import Path
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field


class ArtifactRecord(BaseModel):
    id: str
    sessionId: str = Field(alias="session_id")
    kind: str
    payload: Any
    metadata: Dict[str, Any] = Field(default_factory=dict)
    createdAt: float = Field(alias="created_at")
    updatedAt: float = Field(alias="updated_at")

    model_config = ConfigDict(populate_by_name=True)


class SqliteArtifactStore:
    def __init__(self, path: str = ".runtime/ai-artifacts.sqlite3") -> None:
        self.path = path
        if path != ":memory:":
            Path(path).expanduser().parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()
        self._conn = sqlite3.connect(path, check_same_thread=False)
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS artifacts (
                id TEXT PRIMARY KEY,
                session_id TEXT NOT NULL,
                kind TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                metadata_json TEXT NOT NULL,
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL
            )
            """
        )
        self._conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_artifacts_session ON artifacts(session_id, updated_at)"
        )
        self._conn.commit()

    def create(
        self,
        session_id: str,
        kind: str,
        payload: Any,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> ArtifactRecord:
        now = time.time()
        record = ArtifactRecord(
            id=f"artifact-{uuid.uuid4()}",
            session_id=session_id,
            kind=kind,
            payload=payload,
            metadata=metadata or {},
            created_at=now,
            updated_at=now,
        )
        with self._lock:
            self._conn.execute(
                """
                INSERT INTO artifacts(
                    id, session_id, kind, payload_json, metadata_json, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record.id,
                    record.sessionId,
                    record.kind,
                    json.dumps(record.payload, ensure_ascii=False),
                    json.dumps(record.metadata, ensure_ascii=False),
                    record.createdAt,
                    record.updatedAt,
                ),
            )
            self._conn.commit()
        return record

    def get(self, artifact_id: str) -> Optional[ArtifactRecord]:
        with self._lock:
            row = self._conn.execute(
                """
                SELECT id, session_id, kind, payload_json, metadata_json, created_at, updated_at
                FROM artifacts WHERE id = ?
                """,
                (artifact_id,),
            ).fetchone()
        if not row:
            return None
        return ArtifactRecord(
            id=row[0],
            session_id=row[1],
            kind=row[2],
            payload=json.loads(row[3]),
            metadata=json.loads(row[4]),
            created_at=row[5],
            updated_at=row[6],
        )

    def close(self) -> None:
        with self._lock:
            self._conn.close()
