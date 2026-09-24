from __future__ import annotations

from typing import List, Optional, Sequence

try:
    from langchain_openai import OpenAIEmbeddings
except ImportError:  # pragma: no cover
    OpenAIEmbeddings = None


class OpenAICompatibleEmbeddingProvider:
    """Optional embedding adapter for any OpenAI-compatible embedding endpoint."""

    def __init__(
        self,
        *,
        model: str,
        api_key: str,
        base_url: Optional[str] = None,
    ) -> None:
        if OpenAIEmbeddings is None:
            raise RuntimeError("EMBEDDINGS_UNAVAILABLE: langchain-openai is not installed")
        if not model or not api_key:
            raise ValueError("EMBEDDING_MODEL and EMBEDDING_API_KEY are required")

        kwargs = {
            "model": model,
            "api_key": api_key,
        }
        if base_url:
            kwargs["base_url"] = base_url
        self._client = OpenAIEmbeddings(**kwargs)

    def embed_documents(self, texts: Sequence[str]) -> List[List[float]]:
        return self._client.embed_documents(list(texts))

    def embed_query(self, text: str) -> List[float]:
        return self._client.embed_query(text)
