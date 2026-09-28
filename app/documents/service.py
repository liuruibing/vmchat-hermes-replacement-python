from __future__ import annotations

import hashlib
import json
import os
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.documents.models import DocumentRecord, ParsedDocument


# Browsers normally send application/pdf, but some environments upload an
# otherwise valid PDF as application/octet-stream (or omit Content-Type).  The
# service still verifies both the .pdf filename and the %PDF- file signature,
# so accepting these transport-level MIME variants does not weaken type checks.
PDF_MIME_TYPES = {"application/pdf", "application/x-pdf", "application/octet-stream", ""}


class DocumentService:
    def __init__(
        self,
        *,
        root_dir: str,
        store: Any,
        parser: Any,
        max_document_bytes: int = 20 * 1024 * 1024,
    ) -> None:
        self.root_dir = Path(root_dir)
        self.files_dir = self.root_dir / "files"
        self.parsed_dir = self.root_dir / "parsed"
        self.files_dir.mkdir(parents=True, exist_ok=True)
        self.parsed_dir.mkdir(parents=True, exist_ok=True)
        self.store = store
        self.parser = parser
        self.max_document_bytes = max(1, int(max_document_bytes))

    @staticmethod
    def _safe_filename(filename: str) -> str:
        value = Path(str(filename or "")).name.strip()
        return value or "document.pdf"

    def create_pdf(self, *, filename: str, mime_type: str, content: bytes) -> DocumentRecord:
        safe_name = self._safe_filename(filename)
        normalized_mime = str(mime_type or "").split(";", 1)[0].strip().lower()
        if not safe_name.lower().endswith(".pdf"):
            raise ValueError("UNSUPPORTED_DOCUMENT_TYPE: only PDF files are supported")
        if normalized_mime not in PDF_MIME_TYPES:
            raise ValueError("UNSUPPORTED_DOCUMENT_MIME: only application/pdf is supported")
        if not isinstance(content, (bytes, bytearray)) or not content:
            raise ValueError("EMPTY_DOCUMENT")
        raw = bytes(content)
        if len(raw) > self.max_document_bytes:
            raise ValueError(
                f"DOCUMENT_TOO_LARGE: max {self.max_document_bytes} bytes"
            )
        if not raw.startswith(b"%PDF-"):
            raise ValueError("INVALID_PDF_SIGNATURE")

        document_id = "doc_" + uuid.uuid4().hex
        sha256 = hashlib.sha256(raw).hexdigest()
        file_path = self.files_dir / f"{document_id}.pdf"
        parsed_path = self.parsed_dir / f"{document_id}.json"
        created_at = datetime.now(timezone.utc).isoformat()
        record = DocumentRecord(
            document_id=document_id,
            filename=safe_name,
            mime_type="application/pdf",
            sha256=sha256,
            size_bytes=len(raw),
            page_count=0,
            status="processing",
            file_path=str(file_path),
            parsed_path=None,
            created_at=created_at,
        )
        self.store.put(record)

        tmp_path: Path | None = None
        try:
            fd, temp_name = tempfile.mkstemp(prefix=document_id + "-", suffix=".pdf", dir=str(self.files_dir))
            tmp_path = Path(temp_name)
            with os.fdopen(fd, "wb") as handle:
                handle.write(raw)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(str(tmp_path), str(file_path))
            tmp_path = None

            parsed: ParsedDocument = self.parser.parse(
                file_path,
                document_id=document_id,
                filename=safe_name,
                mime_type="application/pdf",
                sha256=sha256,
                size_bytes=len(raw),
            )
            parsed_path.write_text(
                json.dumps(parsed.model_dump(), ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            ready = record.model_copy(
                update={
                    "status": "ready",
                    "page_count": parsed.page_count,
                    "parsed_path": str(parsed_path),
                    "error": None,
                }
            )
            self.store.put(ready)
            return ready
        except Exception as err:
            if tmp_path is not None:
                try:
                    tmp_path.unlink(missing_ok=True)
                except Exception:
                    pass
            failed = record.model_copy(update={"status": "failed", "error": str(err)[:2000]})
            self.store.put(failed)
            raise

    def get(self, document_id: str) -> DocumentRecord | None:
        return self.store.get(str(document_id or "").strip())

    def require_ready(self, document_id: str) -> DocumentRecord:
        record = self.get(document_id)
        if record is None:
            raise KeyError(f"DOCUMENT_NOT_FOUND: {document_id}")
        if record.status != "ready":
            raise RuntimeError(f"DOCUMENT_NOT_READY: {document_id}")
        return record

    def load_parsed(self, document_id: str) -> ParsedDocument:
        self.require_ready(document_id)
        return self.store.load_parsed(document_id)
