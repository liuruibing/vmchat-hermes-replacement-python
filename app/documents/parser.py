from __future__ import annotations

from pathlib import Path

from app.documents.models import DocumentPage, ParsedDocument


class PdfDocumentParser:
    """Extract text page-by-page while preserving page provenance.

    OCR is deliberately out of scope for the first document-runtime release.
    Scanned PDFs that contain no extractable text fail explicitly so callers do
    not accidentally analyse an empty document.
    """

    def parse(
        self,
        path: str | Path,
        *,
        document_id: str,
        filename: str,
        mime_type: str,
        sha256: str,
        size_bytes: int,
    ) -> ParsedDocument:
        try:
            from pypdf import PdfReader
        except Exception as err:  # pragma: no cover - deployment/configuration guard
            raise RuntimeError(
                "PDF_PARSER_UNAVAILABLE: install the pypdf runtime dependency"
            ) from err

        source = Path(path)
        try:
            reader = PdfReader(str(source), strict=False)
        except Exception as err:
            raise ValueError(f"INVALID_PDF: {err}") from err

        if getattr(reader, "is_encrypted", False):
            try:
                unlocked = reader.decrypt("")
            except Exception:
                unlocked = 0
            if not unlocked:
                raise ValueError("PDF_ENCRYPTED: password-protected PDFs are not supported")

        pages: list[DocumentPage] = []
        text_parts: list[str] = []
        for index, page in enumerate(reader.pages, start=1):
            try:
                text = str(page.extract_text() or "").strip()
            except Exception as err:
                raise ValueError(f"PDF_TEXT_EXTRACTION_FAILED: page {index}: {err}") from err
            pages.append(DocumentPage(page_number=index, text=text))
            if text:
                text_parts.append(f"[Page {index}]\n{text}")

        if not pages:
            raise ValueError("PDF_HAS_NO_PAGES")
        if not text_parts:
            raise ValueError("PDF_NO_EXTRACTABLE_TEXT: OCR is not enabled yet")

        return ParsedDocument(
            document_id=document_id,
            filename=filename,
            mime_type=mime_type,
            sha256=sha256,
            size_bytes=size_bytes,
            page_count=len(pages),
            pages=pages,
            text="\n\n".join(text_parts),
        )
