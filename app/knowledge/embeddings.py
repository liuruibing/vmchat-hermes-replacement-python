# ==============================================================================
# 文件：app/knowledge/embeddings.py
# 文件作用：用 LangChain 的 embedding 客户端把文本转成数字向量，供知识检索比较相似度。
# 全局位置：main.py 创建 embedding Provider → KnowledgeService 建索引/检索 → 本文件 → 向量模型服务。
# 谁调用它：main.py 根据 embedding 配置创建实例，知识服务通过 embed_documents/embed_query 使用它。
# 输入：模型连接配置；建索引时是一组文档文字，检索时是一条查询文字。
# 输出：文档向量列表或查询向量；每个向量是一组浮点数。
# 主要流程：创建 OpenAI 兼容客户端 → 标识向量来源 → 调用文档/查询向量接口。
# 前端类比：像独立的搜索 API service；回答问题的聊天模型客户端在 provider/ 目录中。
# 边界：这里的模型调用是同步的；向量如何保存、排序和组织成上下文由知识服务负责。
# 阅读入口：先看构造方法，再看 fingerprint、embed_documents() 和 embed_query()。
# ==============================================================================

from __future__ import annotations

from typing import List, Optional, Sequence

# embedding 是可选能力；未安装客户端时先允许模块导入，到实际构造时再明确报错。
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

        # kwargs 是命名参数字典；**kwargs 类似展开 options，把 model/api_key 等传给客户端。
        # base_url 可指向 OpenAI 兼容的服务，OpenAIEmbeddings 并不限定服务提供者。
        kwargs = {
            "model": model,
            "api_key": api_key,
        }
        if base_url:
            kwargs["base_url"] = base_url
        # 指纹标明“哪个服务的哪个模型”，供知识索引区分向量来源；它不是文本的向量。
        self.fingerprint = f"openai-compatible:{base_url or 'default'}:{model}"
        self._client = OpenAIEmbeddings(**kwargs)

    # Sequence/List 等是类型提示，不会自动校验数据；每段文档返回一个由浮点数组成的向量。
    # 这是同步调用，执行时会等待模型服务；这里没有 async/await。
    def embed_documents(self, texts: Sequence[str]) -> List[List[float]]:
        return self._client.embed_documents(list(texts))

    # 查询也转成同一模型的向量，检索层才能与文档向量比较，找出意思相近的片段。
    def embed_query(self, text: str) -> List[float]:
        return self._client.embed_query(text)
