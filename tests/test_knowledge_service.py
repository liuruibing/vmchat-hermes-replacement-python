from app.knowledge.service import KnowledgeService
from app.knowledge.store import SqliteKnowledgeStore
import pytest

from app.mandate_risk.models import RawRiskMetric
from app.mandate_risk.registry import RawRiskMetricRegistry


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


def test_metric_knowledge_is_complete_authorized_and_uses_current_registry():
    service = KnowledgeService(SqliteKnowledgeStore(":memory:"))
    first = RawRiskMetric(
        row_id=1, source_row=2, metric_name="信息比率",
        algorithm="IR = (Rp - Rb) / TE", strategy_type="权益",
    )
    second = RawRiskMetric(
        row_id=2, source_row=3, metric_name="跟踪误差",
        algorithm="TE = sigma(Rp - Rb)", strategy_type="权益",
    )
    registry = RawRiskMetricRegistry([first, second], source_path="test-catalogue", source_sha256="v1")
    service.configure_sources("risk-chat", ["risk-metrics"], registry)
    payload = service.context_for_chat("risk-chat", "它的公式是什么", [], "")
    source = payload["sources"][0]
    assert source["complete"] is True
    assert source["total"] == 2
    assert {item["metric_name"] for item in source["items"]} == {"信息比率", "跟踪误差"}
    assert source["items"][0]["algorithm"] == first.algorithm
    assert source["source"] == "test-catalogue"
    assert source["version"] == "v1"
    assert service.context_for_chat("unrelated-chat", "有多少指标", [], "")["sources"] == []

    third = RawRiskMetric(row_id=3, source_row=4, metric_name="新增指标", algorithm="A/B")
    service.configure_sources("risk-chat", ["risk-metrics"], RawRiskMetricRegistry([first, second, third]))
    updated = service.context_for_chat("risk-chat", "全部指标", [], "")["sources"][0]
    assert updated["total"] == 3
    assert updated["items"][-1]["metric_name"] == "新增指标"


def test_unavailable_metric_source_is_not_an_empty_catalogue():
    service = KnowledgeService(SqliteKnowledgeStore(":memory:"))
    service.configure_sources("risk-chat", ["risk-metrics"])
    source = service.context_for_chat("risk-chat", "多少指标", [], "")["sources"][0]
    assert source["status"] == "error"
    assert source["complete"] is False
    assert "total" not in source
    assert "items" not in source
    with pytest.raises(ValueError, match="UNKNOWN_KNOWLEDGE_SOURCE"):
        service.configure_sources("risk-chat", ["missing-source"])


def test_followup_retrieval_uses_recent_user_context_without_cross_agent_leaks():
    service = KnowledgeService(SqliteKnowledgeStore(":memory:"))
    service.index_resource_map("a", {"manual.md": "# 信息比率\n信息比率的分母是跟踪误差。"})
    service.index_resource_map("b", {"secret.md": "# 信息比率\n秘密口径，不可跨 Agent 使用。"})
    result = service.context_for_chat(
        "a", "它的分母是什么",
        [{"role": "user", "content": "解释信息比率"}, {"role": "assistant", "content": "说明"}], "",
    )
    assert "分母是跟踪误差" in result["retrieved_context"]
    assert "秘密口径" not in result["retrieved_context"]


def test_document_retrieval_failure_is_reported_separately_from_metric_knowledge():
    store = SqliteKnowledgeStore(":memory:")
    service = KnowledgeService(store)
    registry = RawRiskMetricRegistry([RawRiskMetric(row_id=1, source_row=2, metric_name="久期")])
    service.configure_sources("a", ["risk-metrics"], registry)
    store.close()
    result = service.context_for_chat("a", "解释久期", [], "")
    assert result["sources"][0]["status"] == "ok"
    assert result["sources"][0]["total"] == 1
    assert result["sources"][1]["status"] == "error"
