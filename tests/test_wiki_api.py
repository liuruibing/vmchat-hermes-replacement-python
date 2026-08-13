import os
import pytest
from fastapi.testclient import TestClient

from app.config import AppConfig
from app.main import create_app
from app.resources.resource_loader import ResourceLoader
from tests.test_resources import RESOURCES_DIR


@pytest.fixture
def wiki_app_client():
    loader = ResourceLoader(RESOURCES_DIR)
    loader.load_sync()
    config = AppConfig(service_api_key="test-key")
    app = create_app({"config": config, "resource_loader": loader})
    client = TestClient(app)
    return client, loader


def test_wiki_unauthenticated_requests_rejected(wiki_app_client):
    client, _ = wiki_app_client
    res = client.get("/v1/wiki/tree")
    assert res.status_code == 403
    assert res.json() == {"error": "FORBIDDEN: Invalid or missing bearer token"}


def test_wiki_tree_success(wiki_app_client):
    client, loader = wiki_app_client
    res = client.get("/v1/wiki/tree", headers={"Authorization": "Bearer test-key"})
    assert res.status_code == 200
    data = res.json()

    resources = loader.get_resources()
    assert data["catalogVersion"] == resources.manifest.catalogVersion
    assert len(data["tree"]) == 1

    root_dir = data["tree"][0]
    assert root_dir["type"] == "directory"
    assert root_dir["name"] == "catalog"
    assert root_dir["path"] == "catalog"

    children = root_dir["children"]
    assert len(children) == 3
    assert children[0] == {
        "type": "file",
        "name": "index.md",
        "path": "catalog/index.md",
        "documentId": "index",
    }
    assert children[1] == {
        "type": "file",
        "name": "metrics.md",
        "path": "catalog/metrics.md",
        "documentId": "metrics",
    }

    modules_dir = children[2]
    assert modules_dir["type"] == "directory"
    assert modules_dir["name"] == "modules"
    assert modules_dir["path"] == "catalog/modules"

    module_children = modules_dir["children"]
    expected_module_ids = sorted(resources.moduleMarkdownMap.keys())
    assert len(module_children) == len(expected_module_ids)

    for i, module_id in enumerate(expected_module_ids):
        assert module_children[i] == {
            "type": "file",
            "name": f"{module_id}.md",
            "path": f"catalog/modules/{module_id}.md",
            "documentId": module_id,
        }


def test_wiki_document_success(wiki_app_client):
    client, loader = wiki_app_client
    headers = {"Authorization": "Bearer test-key"}
    resources = loader.get_resources()

    # Index doc
    index_res = client.get("/v1/wiki/documents/index", headers=headers)
    assert index_res.status_code == 200
    assert index_res.json() == {
        "documentId": "index",
        "path": "catalog/index.md",
        "markdown": resources.catalogIndexMd,
    }

    # Metrics doc
    metrics_res = client.get("/v1/wiki/documents/metrics", headers=headers)
    assert metrics_res.status_code == 200
    assert metrics_res.json() == {
        "documentId": "metrics",
        "path": "catalog/metrics.md",
        "markdown": resources.catalogMetricsMd,
    }

    # Module doc
    first_mod_id = sorted(resources.moduleMarkdownMap.keys())[0]
    mod_res = client.get(f"/v1/wiki/documents/{first_mod_id}", headers=headers)
    assert mod_res.status_code == 200
    assert mod_res.json() == {
        "documentId": first_mod_id,
        "path": f"catalog/modules/{first_mod_id}.md",
        "markdown": resources.moduleMarkdownMap[first_mod_id],
    }


def test_wiki_document_not_found_or_traversal(wiki_app_client):
    client, _ = wiki_app_client
    headers = {"Authorization": "Bearer test-key"}

    unknown_res = client.get("/v1/wiki/documents/unknownId", headers=headers)
    assert unknown_res.status_code == 404
    assert unknown_res.json() == {"error": "WIKI_DOCUMENT_NOT_FOUND"}

    traversal_res = client.get("/v1/wiki/documents/..%2Fskill%2FSKILL.md", headers=headers)
    assert traversal_res.status_code == 404
    assert traversal_res.json() == {"error": "WIKI_DOCUMENT_NOT_FOUND"}


def test_wiki_degraded_when_loader_not_ready():
    loader = ResourceLoader("/nonexistent")
    config = AppConfig(service_api_key="test-key")
    app = create_app({"config": config, "resource_loader": loader})
    client = TestClient(app)

    res = client.get("/v1/wiki/tree", headers={"Authorization": "Bearer test-key"})
    assert res.status_code == 503
    assert res.json() == {"error": "SERVICE_DEGRADED: Resources not loaded"}
