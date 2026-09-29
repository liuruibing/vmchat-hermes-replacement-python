from __future__ import annotations

import re
from typing import List

from pydantic import BaseModel


_PAGE_MARKER_RE = re.compile(r"(?m)^\[Page ([1-9]\d*)\][ \t]*(?:\r?\n|$)")
_SENTENCE_END_RE = re.compile(r"[.!?。！？；;](?=\s|$)")
_SECTION_LABEL_RE = re.compile(r"\d+(?:\.\d+)*\.")
_STRUCTURAL_BOUNDARY_RE = re.compile(
    r"(?m)(?:\r?\n[ \t]*\r?\n|(?<=\n)(?=[ \t]*\d+\)[ \t]+))"
)


class DocumentClause(BaseModel):
    clause_id: str
    text: str
    source_start: int = 0
    source_end: int = 0
    page: int | None = None


def _append_clause(
    clauses: List[DocumentClause],
    source: str,
    start: int,
    end: int,
    *,
    page: int | None = None,
) -> None:
    """Append one exact source span after trimming only outer whitespace."""

    while start < end and source[start].isspace():
        start += 1
    if page is not None:
        # PDF headers sometimes leave the printed page number on its own line
        # immediately before a continued clause. It is not contract text.
        page_label = re.match(rf"{page}[ \t]*\r?\n", source[start:end])
        if page_label:
            start += page_label.end()
            while start < end and source[start].isspace():
                start += 1
    while end > start and source[end - 1].isspace():
        end -= 1
    if start >= end:
        return
    clauses.append(
        DocumentClause(
            clause_id=f"c{len(clauses) + 1:04d}",
            text=source[start:end],
            source_start=start,
            source_end=end,
            page=page,
        )
    )


def _split_sentences(
    clauses: List[DocumentClause],
    source: str,
    start: int,
    end: int,
    *,
    page: int | None,
) -> None:
    cursor = start
    for match in _SENTENCE_END_RE.finditer(source, start, end):
        clause_end = match.end()
        if _SECTION_LABEL_RE.fullmatch(source[cursor:clause_end].strip()):
            continue
        _append_clause(clauses, source, cursor, clause_end, page=page)
        cursor = clause_end
    _append_clause(clauses, source, cursor, end, page=page)


def _split_span(
    clauses: List[DocumentClause],
    source: str,
    start: int,
    end: int,
    *,
    page: int | None,
) -> None:
    cursor = start
    for boundary in _STRUCTURAL_BOUNDARY_RE.finditer(source, start, end):
        _split_sentences(clauses, source, cursor, boundary.start(), page=page)
        cursor = boundary.end()
    _split_sentences(clauses, source, cursor, end, page=page)


def split_document_clauses(document_text: str) -> List[DocumentClause]:
    """Split a document into auditable sentence-level clauses.

    PDF text extraction commonly inserts a newline at every visual line wrap. A
    single newline therefore must *not* be treated as a semantic boundary. We
    split at explicit sentence punctuation, blank paragraphs and numbered list
    items, while preserving any soft line breaks inside a clause.

    ``PdfDocumentParser`` serializes pages into the canonical ``[Page N]`` text
    form. When those markers are present, they are treated as provenance
    boundaries rather than document content: clauses inherit the Python-derived
    page number and never include a page marker or spill across pages. Legacy
    plain-text input without markers keeps the previous behavior with ``page``
    left unset.
    """

    source = str(document_text or "")
    clauses: List[DocumentClause] = []
    page_markers = list(_PAGE_MARKER_RE.finditer(source))

    if page_markers:
        prefix_end = page_markers[0].start()
        if source[:prefix_end].strip():
            _split_span(clauses, source, 0, prefix_end, page=None)

        for index, marker in enumerate(page_markers):
            page = int(marker.group(1))
            start = marker.end()
            end = page_markers[index + 1].start() if index + 1 < len(page_markers) else len(source)
            _split_span(clauses, source, start, end, page=page)
    else:
        _split_span(clauses, source, 0, len(source), page=None)

    if not clauses and source.strip():
        left = len(source) - len(source.lstrip())
        right = len(source.rstrip())
        clauses.append(
            DocumentClause(
                clause_id="c0001",
                text=source[left:right],
                source_start=left,
                source_end=right,
                page=None,
            )
        )
    return clauses
