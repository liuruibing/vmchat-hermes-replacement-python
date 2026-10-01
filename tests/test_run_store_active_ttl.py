from app.runs.run_store import RunStore


def test_active_run_survives_retention_ttl_then_completed_result_expires(monkeypatch):
    now = [100.0]
    monkeypatch.setattr("app.runs.run_store.time.time", lambda: now[0])
    store = RunStore(default_ttl_ms=1000)
    record = store.create()
    assert store.claim(record.id).outcome == "claimed"
    now[0] += 2
    assert store.cleanup() == 0
    assert store.get(record.id) is record
    store.complete(record.id, "report")
    assert store.get(record.id).status == "completed"
    now[0] += 2
    assert store.get(record.id) is None


def test_unclaimed_run_still_expires(monkeypatch):
    now = [100.0]
    monkeypatch.setattr("app.runs.run_store.time.time", lambda: now[0])
    store = RunStore(default_ttl_ms=1000)
    record = store.create()
    now[0] += 2
    assert store.cleanup() == 1
    assert store.get(record.id) is None
