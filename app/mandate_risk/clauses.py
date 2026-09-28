from __future__ import annotations

import re
from typing import List

from pydantic import BaseModel


class DocumentClause(BaseModel):
    clause_id: str
    text: str


def split_document_clauses(document_text: str) -> List[DocumentClause]:
    """Split text into stable, exact-text clauses without rewriting source wording.

    The splitter is intentionally deterministic. It only chooses boundaries; it
    never normalizes or paraphrases the source, so any returned clause can still
    be used as auditable evidence against the original document text.
    """

    source = str(document_text or "")
    clauses: List[DocumentClause] = []
    sequence = 0

    for block in re.split(r"\n+", source):
        block = block.strip()
        if not block:
            continue
        parts = re.split(r"(?<=[.!?。！？；;])\s+", block)
        for part in parts:
            text = part.strip()
            if not text:
                continue
            sequence += 1
            clauses.append(DocumentClause(clause_id=f"c{sequence:04d}", text=text))

    if not clauses and source.strip():
        clauses.append(DocumentClause(clause_id="c0001", text=source.strip()))
    return clauses
