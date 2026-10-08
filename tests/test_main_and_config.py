import json
import pytest
from fastapi.testclient import TestClient

import app.main as main_module
from app.config import load_config, AppConfig
from app.main import create_app, verify_bearer_auth
from app.workflow.registry import WorkflowRegistry


def test_load_config_defaults():
    config = load_config({})
    assert config.host == "127.0.0.1"
    assert config.port == 7310
    assert config.service_api_key == ""
    assert config.llm_provider == "fixed"
    assert config.llm_model == "deepseek-v4-flash"
    assert config.llm_network_retries == 0
    # Test camelCase aliases
    assert config.serviceApiKey == config.service_api_key
    assert config.corsOrigins == config.cors_origins
    assert config.llmProvider == config.llm_provider


def test_load_config_custom_env():
    env = {
        "HOST": "0.0.0.0",
        "PORT": "8080",
        "SERVICE_API_KEY": "mysecret",
        "CORS_ORIGINS": "http://app.com, http://admin.com",
        "LLM_PROVIDER": "langchain",
        "LLM_MODEL": "gpt-4o",
        "LLM_OUTPUT_MODE": "text-json",
        "ALLOW_MISSING_USAGE": "true",
    }
    config = load_config(env)
    assert config.host == "0.0.0.0"
    assert config.port == 8080
    assert config.service_api_key == "mysecret"
    assert config.cors_origins == ["http://app.com", "http://admin.com"]
    assert config.llm_provider == "langchain"
    assert config.llm_model == "gpt-4o"
    assert config.llm_output_mode == "text-json"
    assert config.allow_missing_usage is True


def test_load_config_invalid_network_retries():
    with pytest.raises(ValueError, match="LLM_NETWORK_RETRIES must be 0"):
        load_config({"LLM_NETWORK_RETRIES": "3"})


class MockResourceLoader:
    def __init__(self, ready=True):
        self._ready = ready

    def is_ready(self):
        return self._ready

    def isReady(self):
        return self._ready

    def get_resources(self):
        return {}

    def getResources(self):
        return {}

    async def load(self):
        pass


class Chunk:
    def __init__(self, text):
        self.content_delta = text


class DummyProvider:
    def run_skill(self, *args, **kwargs):
        return [Chunk("hello world")]

    def runSkill(self, *args, **kwargs):
        return [Chunk("hello world")]


def test_health_degraded():
    app = create_app({"resource_loader": MockResourceLoader(ready=False)})
    client = TestClient(app)
    res = client.get("/health")
    assert res.status_code == 503
    data = res.json()
    assert data["status"] == "degraded"
    assert data["skillLoaded"] is False


def test_health_ok():
    app = create_app({"config": AppConfig(), "resource_loader": MockResourceLoader(ready=True)})
    client = TestClient(app)
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"
    assert data["skillLoaded"] is True
    assert data["runtime"]["provider"] == "fixed"
    assert data["runtime"]["modelSelectable"] is False


def test_health_reports_actual_custom_provider_and_workflow_without_secrets():
    from app.workflow.graphs.mandate_risk_v2 import MandateRiskV2Workflow

    provider = DummyProvider()
    provider.runtime_info = {"provider": "omp", "model": "OMP CLI 默认", "api_key": "secret"}
    app = create_app({
        "config": AppConfig(llm_model="misleading-config", llm_api_key="secret"),
        "provider": provider,
        "resource_loader": MockResourceLoader(),
        "workflow_registry": WorkflowRegistry([MandateRiskV2Workflow(mode="screening")]),
    })
    response = TestClient(app).get("/health")
    assert response.json()["runtime"] == {
        "provider": "omp", "model": "OMP CLI 默认", "modelSelectable": False, "v2Mode": "screening",
    }
    assert "secret" not in response.text


def test_run_without_model_uses_provider_default_in_stored_request():
    from app.runs.run_store import RunStore

    store = RunStore()
    provider = DummyProvider()
    provider.model_name = "actual-provider-model"
    app = create_app({
        "config": AppConfig(llm_model="old-config"), "provider": provider,
        "resource_loader": MockResourceLoader(), "run_store": store,
    })
    response = TestClient(app).post("/v1/runs", json={"input": [{"role": "user", "content": "hi"}]})
    assert response.status_code == 200
    record = store.get(response.json()["run_id"])
    assert record.request.model == "actual-provider-model"


def test_bearer_auth():
    config = AppConfig(service_api_key="super-secret")
    app = create_app({"config": config, "resource_loader": MockResourceLoader(ready=True), "provider": DummyProvider()})
    client = TestClient(app)

    # Missing auth header
    res1 = client.post("/v1/runs", json={})
    assert res1.status_code == 403
    assert res1.json()["error"] == "FORBIDDEN: Invalid or missing bearer token"

    # Incorrect token
    res2 = client.post("/v1/runs", json={}, headers={"Authorization": "Bearer wrong-token"})
    assert res2.status_code == 403

    # Correct token
    res3 = client.post("/v1/runs", json={"model": "m", "input": [{"role": "user", "content": "hi"}]}, headers={"Authorization": "Bearer super-secret"})
    assert res3.status_code == 200
    assert "run_id" in res3.json()


def test_runs_create_and_events():
    config = AppConfig(service_api_key="test-key")
    app = create_app({"config": config, "resource_loader": MockResourceLoader(ready=True), "provider": DummyProvider()})
    client = TestClient(app)
    headers = {"Authorization": "Bearer test-key"}

    # Invalid request format (missing model/input)
    res_bad = client.post("/v1/runs", json={"invalid": 123}, headers=headers)
    assert res_bad.status_code == 400
    assert "INVALID_REQUEST" in res_bad.json()["error"]

    # Valid run creation
    res_create = client.post("/v1/runs", json={
        "model": "gpt-4o",
        "input": [{"role": "user", "content": "Hello world"}]
    }, headers=headers)
    assert res_create.status_code == 200
    run_id = res_create.json()["run_id"]

    # Fetch events for non-existent run
    res_404 = client.get("/v1/runs/non-existent-id/events", headers=headers)
    assert res_404.status_code == 404
    assert res_404.json()["error"] == "RUN_NOT_FOUND"

    # Fetch events stream for valid run
    res_events = client.get(f"/v1/runs/{run_id}/events", headers=headers)
    assert res_events.status_code == 200
    assert "text/event-stream" in res_events.headers["content-type"]
    assert "no-transform" in res_events.headers["cache-control"]
    assert "run.completed" in res_events.text


def test_runs_events_forwards_workflow_failure():
    class FailedWorkflow:
        id = "vm-report"

        async def stream(self, _context):
            yield {"event": "run.failed", "error": "DSL 校验失败"}

    app = create_app({
        "resource_loader": MockResourceLoader(ready=True),
        "provider": DummyProvider(),
        "workflow_registry": WorkflowRegistry([FailedWorkflow()]),
    })
    client = TestClient(app)

    res_create = client.post("/v1/runs", json={
        "model": "gpt-4o",
        "input": [{"role": "user", "content": "Hello world"}],
    })
    run_id = res_create.json()["run_id"]

    res_events = client.get(f"/v1/runs/{run_id}/events")
    assert res_events.status_code == 200
    assert '"event":"run.failed"' in res_events.text
    assert '"event":"run.completed"' not in res_events.text


def test_runs_events_preserves_structured_metadata_in_completion_and_replay():
    metadata = {"mandate_risk_v2": {"phase": "complete", "result": {"candidate_metrics": []}}}

    class StructuredWorkflow:
        id = "vm-report"

        async def stream(self, _context):
            yield {"event": "run.completed", "output": "report", "usage": {}, "metadata": metadata}

    app = create_app({"resource_loader": MockResourceLoader(ready=True), "provider": DummyProvider(),
        "workflow_registry": WorkflowRegistry([StructuredWorkflow()])})
    client = TestClient(app)
    run_id = client.post("/v1/runs", json={"model": "m",
        "input": [{"role": "user", "content": "analyze"}]}).json()["run_id"]
    for _ in range(2):
        response = client.get(f"/v1/runs/{run_id}/events")
        events = [json.loads(line[6:]) for line in response.text.splitlines() if line.startswith("data: ")]
        completed = next(item for item in events if item["event"] == "run.completed")
        assert completed["metadata"] == metadata


def test_background_run_polling_preserves_terminal_and_cursor():
    import time

    class Workflow:
        id = "vm-report"

        async def stream(self, _context):
            yield {"event": "reasoning.delta", "delta": "starting", "sequence": 1}
            yield {"event": "run.failed", "error": "quota unavailable"}

    registry = WorkflowRegistry()
    registry.register(Workflow())
    application = create_app({"config": AppConfig(service_api_key="test-key"),
        "resource_loader": MockResourceLoader(ready=True), "provider": DummyProvider(),
        "workflow_registry": registry})
    with TestClient(application) as client:
        headers = {"Authorization": "Bearer test-key"}
        rid = client.post("/v1/runs", headers=headers, json={
            "input": [{"role": "user", "content": "test"}]}).json()["run_id"]
        assert client.post(f"/v1/runs/{rid}/start").status_code == 403
        assert client.post("/v1/runs/missing/start", headers=headers).status_code == 404
        assert client.post(f"/v1/runs/{rid}/start", headers=headers).status_code == 202
        snapshot = None
        for _ in range(30):
            snapshot = client.get(f"/v1/runs/{rid}/snapshot", headers=headers).json()
            if snapshot["status"] == "failed":
                break
            time.sleep(0.01)
        events = [json.loads(frame[6:]) for frame in snapshot["frames"]]
        assert [event["event"] for event in events] == ["reasoning.delta", "run.failed"]
        assert events[-1]["error"] == "quota unavailable"
        assert client.post(f"/v1/runs/{rid}/start", headers=headers).status_code == 200
        assert client.get(f"/v1/runs/{rid}/snapshot", headers=headers,
            params={"after": snapshot["cursor"]}).json()["frames"] == []
        assert client.get(f"/v1/runs/{rid}/snapshot", headers=headers,
            params={"after": -1}).status_code == 400
        assert client.get(f"/v1/runs/{rid}/snapshot").status_code == 403


def test_background_run_can_be_cancelled_and_success_polls_in_pages():
    import asyncio
    import time

    class Workflow:
        id = "vm-report"

        async def stream(self, context):
            yield {"event": "reasoning.delta", "delta": "start", "sequence": 1}
            if context.input_val.userMessage == "wait":
                await asyncio.sleep(60)
            for _ in range(105):
                yield {"event": "message.delta", "delta": "x"}
            yield {"event": "run.completed", "output": "x" * 105,
                   "metadata": {"verified": True}}

    registry = WorkflowRegistry()
    registry.register(Workflow())
    application = create_app({"resource_loader": MockResourceLoader(ready=True),
        "provider": DummyProvider(), "workflow_registry": registry})
    with TestClient(application) as client:
        def start(prompt):
            rid = client.post("/v1/runs", json={
                "input": [{"role": "user", "content": prompt}]}).json()["run_id"]
            assert client.post(f"/v1/runs/{rid}/start").status_code == 202
            return rid

        rid = start("wait")
        assert client.post(f"/v1/runs/{rid}/cancel").status_code == 200
        for _ in range(30):
            snapshot = client.get(f"/v1/runs/{rid}/snapshot").json()
            if snapshot["status"] == "failed":
                break
            time.sleep(0.01)
        assert snapshot["status"] == "failed"
        assert "客户端连接已中断" in snapshot["frames"][-1]

        rid = start("finish")
        for _ in range(30):
            snapshot = client.get(f"/v1/runs/{rid}/snapshot").json()
            if snapshot["status"] == "completed":
                break
            time.sleep(0.01)
        assert snapshot["status"] == "completed"
        assert len(snapshot["frames"]) == 100
        rest = client.get(f"/v1/runs/{rid}/snapshot",
            params={"after": snapshot["cursor"]}).json()
        terminal = json.loads(rest["frames"][-1][6:])
        assert terminal["event"] == "run.completed"
        assert terminal["metadata"] == {"verified": True}
