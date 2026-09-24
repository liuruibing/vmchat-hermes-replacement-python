from app.knowledge.service import KnowledgeService
from app.knowledge.store import SqliteKnowledgeStore


def test_knowledge_service_indexes_and_retrieves_relevant_chunks():
    store = SqliteKnowledgeStore(":memory:")
    service = KnowledgeService(store)

    stats = service.index_resource_map(
        "performance-ai",
        {
            "catalog/pe.md": "# 持仓平均PE\n持仓平均PE按估值日期形成时间序列，原始字段 F_PETTM。",
            "catalog/duration.md": "# 组合久期\n组合久期用于固定收益组合久期分析。",
            "catalog/unrelated.md": "# 产品基本信息\n产品名称、管理人和成立日期。",
        },
    )

    assert stats["documents"] == 3
    hits = service.search("performance-ai", "持仓平均PE PE", limit=3)
    assert hits
    assert hits[0].path == "catalog/pe.md"
    assert "F_PETTM" in hits[0].content


def test_knowledge_reindex_skips_unchanged_documents():
    store = SqliteKnowledgeStore(":memory:")
    service = KnowledgeService(store)
    docs = {"wiki/a.md": "# A\n组合久期"}

    first = service.index_resource_map("a", docs)
    second = service.index_resource_map("a", docs)

    assert first["documents"] == 1
    assert second["documents"] == 0
