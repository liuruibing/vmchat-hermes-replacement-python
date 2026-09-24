from __future__ import annotations

import hashlib
import json
import math
import re
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence

try:
    import duckdb
except Exception:  # pragma: no cover - optional until runtime dependency is installed
    duckdb = None


@dataclass
class KnowledgeChunk:
    chunk_id: str
    agent_id: str
    path: str
    title: str
    content: str
    metadata: Dict[str, Any]
    checksum: str
    embedding: Optional[List[float]] = None


@dataclass
class KnowledgeSearchHit:
    chunk_id: str
    path: str
    title: str
    content: str
    score: float
    metadata: Dict[str, Any]


def _cosine(a: Sequence[float], b: Sequence[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na <= 0 or nb <= 0:
        return 0.0
    return dot / (na * nb)


class DuckDbKnowledgeStore:
    """Embedded knowledge index.

    DuckDB stores chunks, metadata and optional vectors in one local file. The
    implementation deliberately avoids requiring the VSS extension: vector
    ranking falls back to application-side cosine similarity for the small/
    medium corpora this framework targets. The backend can later be swapped
    behind the same interface for pgvector/Qdrant/Milvus.
    """

    def __init__(self, path: str = ".runtime/knowledge.duckdb") -> None:
        if duckdb is None:
            raise RuntimeError(
                "DUCKDB_NOT_INSTALLED: install project dependencies before using KnowledgeService"
            )
        self.path = path
        if path != ":memory:":
            Path(path).expanduser().parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()
        self._conn = duckdb.connect(path)
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS knowledge_chunks (
                chunk_id VARCHAR PRIMARY KEY,
                agent_id VARCHAR NOT NULL,
                path VARCHAR NOT NULL,
                title VARCHAR NOT NULL,
                content VARCHAR NOT NULL,
                metadata_json VARCHAR NOT NULL,
                checksum VARCHAR NOT NULL,
                embedding_json VARCHAR
            )
            """
        )
        self._conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_knowledge_agent ON knowledge_chunks(agent_id)"
        )
        self._conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_knowledge_path ON knowledge_chunks(agent_id, path)"
        )

    def existing_checksums(self, agent_id: str) -> Dict[str, str]:
        with self._lock:
            rows = self._conn.execute(
                """
                SELECT path, max(checksum)
                FROM knowledge_chunks
                WHERE agent_id = ?
                GROUP BY path
                """,
                [agent_id],
            ).fetchall()
        return {str(path): str(checksum) for path, checksum in rows}

    def replace_document(
        self,
        agent_id: str,
        path: str,
        chunks: Sequence[KnowledgeChunk],
    ) -> None:
        with self._lock:
            self._conn.execute(
                "DELETE FROM knowledge_chunks WHERE agent_id = ? AND path = ?",
                [agent_id, path],
            )
            if chunks:
                self._conn.executemany(
                    """
                    INSERT INTO knowledge_chunks(
                        chunk_id, agent_id, path, title, content,
                        metadata_json, checksum, embedding_json
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    [
                        [
                            chunk.chunk_id,
                            chunk.agent_id,
                            chunk.path,
                            chunk.title,
                            chunk.content,
                            json.dumps(chunk.metadata, ensure_ascii=False),
                            chunk.checksum,
                            json.dumps(chunk.embedding) if chunk.embedding is not None else None,
                        ]
                        for chunk in chunks
                    ],
                )

    def search(
        self,
        agent_id: str,
        query_terms: Sequence[str],
        limit: int = 8,
        query_embedding: Optional[Sequence[float]] = None,
    ) -> List[KnowledgeSearchHit]:
        with self._lock:
            rows = self._conn.execute(
                """
                SELECT chunk_id, path, title, content, metadata_json, embedding_json
                FROM knowledge_chunks
                WHERE agent_id = ?
                """,
                [agent_id],
            ).fetchall()

        lowered_terms = [term.lower() for term in query_terms if term]
        hits: List[KnowledgeSearchHit] = []
        for chunk_id, path, title, content, metadata_json, embedding_json in rows:
            haystack = f"{title}\n{content}".lower()
            lexical = 0.0
            for term in lowered_terms:
                if term in haystack:
                    lexical += 1.0
                    if term in str(title).lower():
                        lexical += 0.75

            vector_score = 0.0
            if query_embedding is not None and embedding_json:
                try:
                    vector_score = max(
                        0.0,
                        _cosine(query_embedding, json.loads(embedding_json)),
                    )
                except Exception:
                    vector_score = 0.0

            if lexical <= 0 and vector_score <= 0:
                continue

            lexical_norm = lexical / max(1.0, float(len(lowered_terms)))
            score = lexical_norm * 0.70 + vector_score * 0.30
            hits.append(
                KnowledgeSearchHit(
                    chunk_id=str(chunk_id),
                    path=str(path),
                    title=str(title),
                    content=str(content),
                    score=score,
                    metadata=json.loads(metadata_json or "{}"),
                )
            )

        hits.sort(key=lambda item: item.score, reverse=True)
        return hits[: max(1, limit)]

    def close(self) -> None:
        with self._lock:
            self._conn.close()
