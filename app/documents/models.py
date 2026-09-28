from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class DocumentPage(BaseModel):
    page_number: int = Field(ge=1)
    text: str = ""


class ParsedDocument(BaseModel):
    document_id: str
    filename: str
    mime_type: str = "application/pdf"
    sha256: str
    size_bytes: int = Field(ge=0)
    page_count: int = Field(ge=0)
    pages: List[DocumentPage] = Field(default_factory=list)
    text: str = ""


class DocumentRecord(BaseModel):
    document_id: str
    filename: str
    mime_type: str
    sha256: str
    size_bytes: int
    page_count: int = 0
    status: Literal["processing", "ready", "failed"] = "processing"
    file_path: str
    parsed_path: Optional[str] = None
    created_at: str
    error: Optional[str] = None

    def public_dict(self) -> dict:
        return {
            "document_id": self.document_id,
            "filename": self.filename,
            "mime_type": self.mime_type,
            "sha256": self.sha256,
            "size_bytes": self.size_bytes,
            "page_count": self.page_count,
            "status": self.status,
            "created_at": self.created_at,
            "error": self.error,
        }
