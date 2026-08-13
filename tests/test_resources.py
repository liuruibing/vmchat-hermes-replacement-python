import asyncio
import os
import tempfile
import pytest
from app.resources import (
    ResourceLoader,
    SkillResourceReader,
    SkillResourceReaderOptions,
)

RESOURCES_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../vmchat-hermes-replacement/resources")
)


def test_resource_loader_sync():
    loader = ResourceLoader(RESOURCES_DIR)
    assert not loader.is_ready()
    with pytest.raises(RuntimeError, match="NOT_READY"):
        loader.get_resources()

    resources = loader.load_sync()
    assert loader.is_ready()
    assert resources.manifest.moduleCount == 36
    assert "catalog/index.md" in resources.toolResourceTextByPath
    assert "catalog/metrics.md" in resources.toolResourceTextByPath
    assert "catalog/execution-contract.json" in resources.toolResourceTextByPath


def test_skill_requires_business_info_protocol_for_knowledge_queries():
    resources = ResourceLoader(RESOURCES_DIR).load_sync()
    skill = resources.skillMd

    assert "## 业务信息展示协议" in skill
    assert '"intent": "businessInfo"' in skill
    assert '"renderType": "businessInfo"' in skill
    assert "不得生成 DSL，不得请求数据" in skill
    assert "不要因为当前已有报告块改变分类" in skill


def test_resource_loader_async():
    async def _run():
        loader = ResourceLoader(RESOURCES_DIR)
        resources = await loader.load()
        assert loader.is_ready()
        assert resources.manifest.moduleCount == 36

    asyncio.run(_run())


def test_resource_loader_missing_manifest():
    with tempfile.TemporaryDirectory() as tmpdir:
        loader = ResourceLoader(tmpdir)
        with pytest.raises(RuntimeError, match="MISSING_MANIFEST"):
            loader.load_sync()


def test_skill_resource_reader_valid():
    loader = ResourceLoader(RESOURCES_DIR)
    resources = loader.load_sync()

    reader = SkillResourceReader(
        resources,
        SkillResourceReaderOptions(maxContextChars=100_000, initialContextChars=1_000),
    )

    catalog_index = reader.read("catalog/index.md")
    assert "# VM 模块索引" in catalog_index

    metrics = reader.read("catalog/metrics.md")
    assert len(metrics) > 0

    contract = reader.read("catalog/execution-contract.json")
    assert "modules" in contract

    read_map = reader.get_read_resources()
    assert "catalog/index.md" in read_map
    assert "catalog/metrics.md" in read_map


def test_skill_resource_reader_restrictions():
    loader = ResourceLoader(RESOURCES_DIR)
    resources = loader.load_sync()

    reader = SkillResourceReader(
        resources,
        SkillResourceReaderOptions(maxContextChars=100_000, initialContextChars=1_000),
    )

    assert reader.read("schemas/dsl.schema.json") == "RESOURCE_NOT_ALLOWED"
    assert reader.read("skill/SKILL.md") == "RESOURCE_NOT_ALLOWED"
    assert reader.read("/etc/passwd") == "RESOURCE_NOT_ALLOWED"
    assert reader.read("../catalog/index.md") == "RESOURCE_NOT_ALLOWED"
    assert reader.read("catalog\\index.md") == "RESOURCE_NOT_ALLOWED"
    assert reader.read("catalog/modules/unknownModule.md") == "RESOURCE_NOT_ALLOWED"

    assert len(reader.get_read_resources()) == 0


def test_skill_resource_reader_already_read():
    loader = ResourceLoader(RESOURCES_DIR)
    resources = loader.load_sync()

    reader = SkillResourceReader(
        resources,
        SkillResourceReaderOptions(maxContextChars=100_000, initialContextChars=1_000),
    )

    first = reader.read("catalog/index.md")
    assert first != "RESOURCE_ALREADY_READ"

    second = reader.read("catalog/index.md")
    assert second == "RESOURCE_ALREADY_READ"

    assert len(reader.get_read_resources()) == 1


def test_skill_resource_reader_context_too_large():
    loader = ResourceLoader(RESOURCES_DIR)
    resources = loader.load_sync()

    reader = SkillResourceReader(
        resources,
        SkillResourceReaderOptions(maxContextChars=1_005, initialContextChars=1_000),
    )

    res = reader.read("catalog/index.md")
    assert res == "RESOURCE_CONTEXT_TOO_LARGE"
    assert len(reader.get_read_resources()) == 0
