from __future__ import annotations

import re
from typing import List

from pydantic import BaseModel


class DocumentClause(BaseModel):
    clause_id: str
    text: str
    source_start: int = 0
    source_end: int = 0


def _append_clause(
    clauses: List[DocumentClause],
    source: str,
    start: int,
    end: int,
) -> None:
    """Append one exact source span after trimming only outer whitespace."""

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
        )
    )


def split_document_clauses(document_text: str) -> List[DocumentClause]:
    """Split a document into auditable sentence-level clauses.

    PDF text extraction commonly inserts a newline at every visual line wrap. A
    single newline therefore must *not* be treated as a semantic boundary. We
    split at explicit sentence punctuation and preserve the exact source span,
    including any soft line breaks inside the sentence. This lets matching use
    whitespace-normalized text while validators/renderers can still point back
    to verbatim source text.
    """

    source = str(document_text or "")
    clauses: List[DocumentClause] = []
    start = 0

    # A sentence terminator is a reliable boundary even when the following
    # whitespace contains one or more PDF line wraps.
    for match in re.finditer(r"[.!?。！？；;](?=\s|$)", source):
        end = match.end()
        _append_clause(clauses, source, start, end)
        start = end

    # Keep any trailing heading/text that has no terminal punctuation.
    _append_clause(clauses, source, start, len(source))

    if not clauses and source.strip():
        left = len(source) - len(source.lstrip())
        right = len(source.rstrip())
        clauses.append(
            DocumentClause(
                clause_id="c0001",
                text=source[left:right],
                source_start=left,
                source_end=right,
            )
        )
    return clauses
