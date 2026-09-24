from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Mapping, Optional, Protocol, Sequence

from app.knowledge.store import DuckDbKnowledgeStore, KnowledgeChunk, KnowledgeSearchHit


class EmbeddingProvider(Protocol):
    def embed_documents(self, texts: Sequence[str]) -> List[List[float]]:
        ...

    def embed_query(self, text: str) -> List[float]:
        ...


@dataclass
class KnowledgeSearchResult:
    path: str
    title: str
    content: str
    score: float
    metadata: Dict[str, Any]


def _search_terms(query: str, max_terms: int = 24) -> List[str]:
    source = str(query or "").strip().lower()
    terms: List[str] = []

    for token in re.findall(r"[a-z0-9_]{2,}|[\u3400-\u9fff]{2,}", source):
        if token not in terms:
            terms.append(token)

        if re.fullmatch(r"[\u3400-\u9fff]{4,}", token):
            for size in (4, 3, 2):
                for index in range(len(token) - size + 1):
                    gram = token[index:index + size]
                    if gram not in terms:
                        terms.append(gram)
                    if len(terms) >= max_terms:
                        return terms[:max_terms]

    return terms[:max_terms]


def _chunk_markdown(
    path: str,
    text: str,
    max_chars: int = 1800,
    overlap_chars: int = 160,
) -> List[tuple[str, str]]:
    lines = str(text or "").splitlines()
    sections: List[tuple[str, str]] = []
    heading = path
    buffer: List[str] = []

    def flush() -> None:
        nonlocal buffer
        body = "\n".join(buffer).strip()
        if body:
            sections.append((heading, body))
        buffer = []

    for line in lines:
        if line.lstrip().startswith("#"):
            flush()
            clean = line.lstrip("#").strip()
            heading = clean or path
            buffer.append(line)
        else:
            buffer.append(line)
    flush()

    chunks: List[tuple[str, str]] = []
    for title, section in sections or [(path, str(text or ""))]:
        if len(section) <= max_chars:
            chunks.append((title, section))
            continue

        start = 0
        while start < len(section):
            end = min(len(section), start + max_chars)
            chunk = section[start:end].strip()
            if chunk:
                chunks.append((title, chunk))
            if end >= len(section):
                break
            start = max(start + 1, end - overlap_chars)

    return chunks


class KnowledgeService:
    def __init__(
        self,
        store: DuckDbKnowledgeStore,
        embedder: Optional[EmbeddingProvider] = None,
    ) -> None:
        self.store = store
        self.embedder = embedder

    def index_resource_map(
        self,
        agent_id: str,
        resources: Mapping[str, str],
    ) -> Dict[str, int]:
        existing = self.store.existing_checksums(agent_id)
        indexed_docs = 0
        indexed_chunks = 0

        for path, content in resources.items():
            raw = str(content or "")
            checksum = hashlib.sha256(raw.encode("utf-8")).hexdigest()
            if existing.get(path) == checksum:
                continue

            raw_chunks = _chunk_markdown(path, raw)
            embeddings: Optional[List[List[float]]] = None
            if self.embedder and raw_chunks:
                try:
                    embeddings = self.embedder.embed_documents(
                        [chunk_text for _, chunk_text in raw_chunks]
                    )
                except Exception:
                    embeddings = None

            chunks: List[KnowledgeChunk] = []
            for index, (title, chunk_text) in enumerate(raw_chunks):
                chunk_id = hashlib.sha256(
                    f"{agent_id}\0{path}\0{index}\0{checksum}".encode("utf-8")
                ).hexdigest()
                embedding = (
                    embeddings[index]
                    if embeddings is not None and index < len(embeddings)
                    else None
                )
                chunks.append(
                    KnowledgeChunk(
                        chunk_id=chunk_id,
                        agent_id=agent_id,
                        path=path,
                        title=title,
                        content=chunk_text,
                        metadata={"chunkIndex": index},
                        checksum=checksum,
                        embedding=embedding,
                    )
                )

            self.store.replace_document(agent_id, path, chunks)
            indexed_docs += 1
            indexed_chunks += len(chunks)

        return {"documents": indexed_docs, "chunks": indexed_chunks}

    def search(
        self,
        agent_id: str,
        query: str,
        limit: int = 8,
    ) -> List[KnowledgeSearchResult]:
        terms = _search_terms(query)
        query_embedding = None
        if self.embedder:
            try:
                query_embedding = self.embedder.embed_query(query)
            except Exception:
                query_embedding = None

        hits = self.store.search(
            agent_id=agent_id,
            query_terms=terms,
            limit=limit,
            query_embedding=query_embedding,
        )
        return [
            KnowledgeSearchResult(
                path=hit.path,
                title=hit.title,
                content=hit.content,
                score=hit.score,
                metadata=hit.metadata,
            )
            for hit in hits
        ]

    def format_for_tool(
        self,
        agent_id: str,
        query: str,
        limit: int = 6,
        max_chars: int = 12000,
    ) -> str:
        hits = self.search(agent_id=agent_id, query=query, limit=limit)
        if not hits:
            return "KNOWLEDGE_NOT_FOUND"

        parts: List[str] = []
        used = 0
        for hit in hits:
            chunk = (
                f"--- {hit.path} :: {hit.title} :: score={hit.score:.3f} ---\n"
                f"{hit.content}"
            )
            if parts and used + len(chunk) > max_chars:
                break
            parts.append(chunk)
            used += len(chunk)

        return "\n\n".join(parts) if parts else "KNOWLEDGE_NOT_FOUND"
