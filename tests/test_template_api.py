from pathlib import Path

from fastapi.testclient import TestClient

from app.config import AppConfig
from app.main import create_app
from app.template_store import TemplateStore


def test_template_crud_is_persistent(tmp_path: Path):
    template_file = tmp_path / "templates.json"
    config = AppConfig(service_api_key="test-key", templates_file=str(template_file))
    store = TemplateStore(template_file)
    app = create_app({"config": config, "template_store": store})
    client = TestClient(app)
    headers = {"Authorization": "Bearer test-key"}
    template = {
        "id": "vm-template-1",
        "title": "净值走势",
        "entityType": "vm-block-template",
        "payload": {"blockId": "block-1"},
        "updatedBy": "测试用户",
    }

    assert client.get("/v1/templates").status_code == 403

    created = client.post("/v1/templates", json=template, headers=headers)
    assert created.status_code == 200
    assert created.json()["template"]["id"] == template["id"]
    assert template_file.exists()

    fetched = client.get("/v1/templates/vm-template-1", headers=headers)
    assert fetched.status_code == 200
    assert fetched.json()["template"]["payload"] == template["payload"]

    updated = dict(template, title="净值走势图")
    replaced = client.put("/v1/templates/vm-template-1", json=updated, headers=headers)
    assert replaced.status_code == 200
    assert replaced.json()["template"]["title"] == "净值走势图"

    deleted = client.delete("/v1/templates/vm-template-1", headers=headers)
    assert deleted.status_code == 200
    assert client.get("/v1/templates/vm-template-1", headers=headers).status_code == 404


def test_template_batch_replace_filters_invalid_records(tmp_path: Path):
    config = AppConfig(templates_file=str(tmp_path / "templates.json"))
    app = create_app({"config": config, "template_store": TemplateStore(config.templates_file)})
    client = TestClient(app)

    response = client.put(
        "/v1/templates",
        json={
            "templates": [
                {"id": "valid", "entityType": "vm-block-template", "title": "有效"},
                {"id": "valid", "entityType": "vm-block-template", "title": "重复"},
                {"title": "缺少 id"},
            ]
        },
    )
    assert response.status_code == 200
    assert response.json()["templates"] == [{"id": "valid", "entityType": "vm-block-template", "title": "有效"}]
