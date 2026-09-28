from __future__ import annotations

import json
import sqlite3
import threading
from pathlib import Path
from typing import Optional

from app.documents.models import DocumentRecord, ParsedDocument


class SqliteDocumentStore:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        if db_path != ":memory:":
            Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._lock = threading.RLock()
        with self._lock:
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS documents (
                    document_id TEXT PRIMARY KEY,
                    filename TEXT NOT NULL,
                    mime_type TEXT NOT NULL,
                    sha256 TEXT NOT NULL,
                    size_bytes INTEGER NOT NULL,
                    page_count INTEGER NOT NULL DEFAULT 0,
                    status TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    parsed_path TEXT,
                    created_at TEXT NOT NULL,
                    error TEXT
                )
                """
            )
            self._conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_documents_sha256 ON documents(sha256)"
            )
            self._conn.commit()

    def put(self, record: DocumentRecord) -> DocumentRecord:
        with self._lock:
            self._conn.execute(
                """
                INSERT OR REPLACE INTO documents (
                    document_id, filename, mime_type, sha256, size_bytes,
                    page_count, status, file_path, parsed_path, created_at, error
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record.document_id,
                    record.filename,
                    record.mime_type,
                    record.sha256,
                    record.size_bytes,
                    record.page_count,
                    record.status,
                    record.file_path,
                    record.parsed_path,
                    record.created_at,
                    record.error,
                ),
            )
            self._conn.commit()
        return record

    def get(self, document_id: str) -> Optional[DocumentRecord]:
        with self._lock:
            row = self._conn.execute(
                "SELECT * FROM documents WHERE document_id = ?",
                (document_id,),
            ).fetchone()
        return DocumentRecord.model_validate(dict(row)) if row else None

    def load_parsed(self, document_id: str) -> ParsedDocument:
        record = self.get(document_id)
        if record is None:
            raise KeyError(f"DOCUMENT_NOT_FOUND: {document_id}")
        if record.status != "ready" or not record.parsed_path:
            raise RuntimeError(f"DOCUMENT_NOT_READY: {document_id}")
        path = Path(record.parsed_path)
        if not path.is_file():
            raise RuntimeError(f"DOCUMENT_PARSED_FILE_MISSING: {document_id}")
        return ParsedDocument.model_validate(json.loads(path.read_text(encoding="utf-8")))

    def close(self) -> None:
        with self._lock:
            self._conn.close()
