from __future__ import annotations

import json
from pathlib import Path
import tempfile

import pytest

from app.mandate_risk_v2.reference_portfolio import (
    ReferencePortfolioItem,
    ReferencePortfolioResolver,
    ReferencePortfolioSource,
)


DEFAULT_TEST_MAPPING_DATA = {
    "schema_version": 1,
    "mappings": {
        "基金收益率": "F_PYIELD",
        "超额收益率（基准超额）": "F_EXCESS_YIELD",
        "Alpha": "F_ALPHA",
        "组合收益率": "F_PYIELD",
        "超额收益率": "F_EXCESS_YIELD",
    },
}


def _create_isolated_env(tmpdir: Path, snapshot_data: dict, mapping_data: dict | None = None) -> tuple[Path, Path]:
    snap_path = tmpdir / "isolated_snapshot.json"
    snap_path.write_text(json.dumps(snapshot_data), encoding="utf-8")
    map_path = tmpdir / "isolated_mapping.json"
    map_path.write_text(json.dumps(mapping_data if mapping_data is not None else DEFAULT_TEST_MAPPING_DATA), encoding="utf-8")
    return snap_path, map_path


def test_distinguish_unknown_mapping_vs_unavailable_snapshot():
    """Clear distinction between unmapped metrics (ready snapshot) and missing snapshot (unavailable)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        snap_data = {
            "schema_version": 1,
            "exported_at": "2026-10-12T00:00:00Z",
            "configs": [
                {"id": "c1", "port_code": "P1", "port_name": "组合1", "effective_date": "2026-01-01"},
            ],
            "details": [
                {"id": "d1", "config_id": "c1", "index_code": "F_ALPHA", "index_name": "Alpha", "index_type": "core"},
            ],
        }
        snap_path, map_path = _create_isolated_env(tmp_path, snap_data)

        # 1. Snapshot ready, but metric has no mapping
        ready_resolver = ReferencePortfolioResolver(
            snapshot_path=snap_path, mapping_path=map_path, as_of_date="2026-10-12",
        )
        assert ready_resolver.is_ready() is True
        assert ready_resolver.get_source().status == "ready"
        assert ready_resolver.get_index_code("信息比率") is None
        assert ready_resolver.get_index_code("跟踪误差") is None
        assert ready_resolver.resolve("信息比率") == []
        # Mapped metric resolves normally
        assert [p.port_code for p in ready_resolver.resolve("Alpha")] == ["P1"]

        # 2. Snapshot file is nonexistent
        missing_snap_resolver = ReferencePortfolioResolver(
            snapshot_path=tmp_path / "nonexistent_snapshot.json",
            mapping_path=map_path,
            as_of_date="2026-10-12",
        )
        assert missing_snap_resolver.is_ready() is False
        assert missing_snap_resolver.get_source().status == "unavailable"
        assert missing_snap_resolver.get_source().snapshot_exported_at is None
        assert missing_snap_resolver.resolve("Alpha") == []


def test_mapping_missing_corrupt_or_non_object_status_unavailable():
    """Missing, corrupt, non-object, or invalid mapping must result in status unavailable."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        snap_data = {
            "schema_version": 1,
            "exported_at": "2026-10-12T00:00:00Z",
            "configs": [{"id": "c1", "port_code": "P1", "port_name": "组合1", "effective_date": "2026-01-01"}],
            "details": [{"id": "d1", "config_id": "c1", "index_code": "F_ALPHA", "index_name": "Alpha", "index_type": "core"}],
        }
        snap_path = tmp_path / "snapshot.json"
        snap_path.write_text(json.dumps(snap_data), encoding="utf-8")

        # 1. Missing mapping file
        missing_map = ReferencePortfolioResolver(
            snapshot_path=snap_path, mapping_path=tmp_path / "missing_mapping.json", as_of_date="2026-10-12",
        )
        assert missing_map.is_ready() is False
        assert missing_map.get_source().status == "unavailable"
        assert missing_map.resolve("Alpha") == []

        # 2. Corrupt mapping JSON
        corrupt_map_path = tmp_path / "corrupt_mapping.json"
        corrupt_map_path.write_text("{not valid json", encoding="utf-8")
        corrupt_resolver = ReferencePortfolioResolver(
            snapshot_path=snap_path, mapping_path=corrupt_map_path, as_of_date="2026-10-12",
        )
        assert corrupt_resolver.is_ready() is False
        assert corrupt_resolver.get_source().status == "unavailable"
        assert corrupt_resolver.resolve("Alpha") == []

        # 3. Non-object root
        array_map_path = tmp_path / "array_mapping.json"
        array_map_path.write_text("[]", encoding="utf-8")
        array_resolver = ReferencePortfolioResolver(
            snapshot_path=snap_path, mapping_path=array_map_path, as_of_date="2026-10-12",
        )
        assert array_resolver.is_ready() is False
        assert array_resolver.get_source().status == "unavailable"

        # 4. 'mappings' field is not an object
        bad_field_path = tmp_path / "bad_field_mapping.json"
        bad_field_path.write_text(json.dumps({"mappings": "invalid_string"}), encoding="utf-8")
        bad_field_resolver = ReferencePortfolioResolver(
            snapshot_path=snap_path, mapping_path=bad_field_path, as_of_date="2026-10-12",
        )
        assert bad_field_resolver.is_ready() is False
        assert bad_field_resolver.get_source().status == "unavailable"


def test_historical_alpha_vs_excess_change():
    """Verify historical version shift across dates in an isolated environment."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        snap_data = {
            "schema_version": 1,
            "exported_at": "2026-10-12T00:00:00Z",
            "configs": [
                {
                    "id": "c100-2025",
                    "port_code": "C100",
                    "port_name": "组合100",
                    "effective_date": "2025-01-01",
                    "updated_at": "2025-01-01T00:00:00",
                },
                {
                    "id": "c100-2026",
                    "port_code": "C100",
                    "port_name": "组合100",
                    "effective_date": "2026-01-01",
                    "updated_at": "2026-01-01T00:00:00",
                },
                {
                    "id": "c101-2026",
                    "port_code": "C101",
                    "port_name": "组合101",
                    "effective_date": "2026-09-16",
                    "updated_at": "2026-09-16T00:00:00",
                },
            ],
            "details": [
                {"id": "d1", "config_id": "c100-2025", "index_code": "F_EXCESS_YIELD", "index_name": "超额收益率", "index_type": "core"},
                {"id": "d2", "config_id": "c100-2026", "index_code": "F_ALPHA", "index_name": "Alpha", "index_type": "core"},
                {"id": "d3", "config_id": "c101-2026", "index_code": "F_EXCESS_YIELD", "index_name": "超额收益率", "index_type": "core"},
            ],
        }
        snap_path, map_path = _create_isolated_env(tmp_path, snap_data)

        # On 2025-06-01: C100 had 2025 config containing F_EXCESS_YIELD, NO Alpha; C101 not yet started
        r2025 = ReferencePortfolioResolver(snapshot_path=snap_path, mapping_path=map_path, as_of_date="2025-06-01")
        assert [p.port_code for p in r2025.resolve("超额收益率（基准超额）")] == ["C100"]
        assert [p.port_code for p in r2025.resolve("Alpha")] == []

        # On 2026-10-12: C100 current config is 2026-01-01 (Alpha, NO Excess Yield); C101 has Excess Yield
        r2026 = ReferencePortfolioResolver(snapshot_path=snap_path, mapping_path=map_path, as_of_date="2026-10-12")
        assert [p.port_code for p in r2026.resolve("Alpha")] == ["C100"]
        assert [p.port_code for p in r2026.resolve("超额收益率（基准超额）")] == ["C101"]


def test_version_precedence_and_parent_expired_nuance():
    """Parent nuance: older END_DATE=null must NOT reappear when a newer already-started config expires."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        snap_data = {
            "schema_version": 1,
            "exported_at": "2026-10-12T00:00:00Z",
            "configs": [
                {
                    "id": "cfg-old",
                    "port_code": "PORT_A",
                    "port_name": "组合A",
                    "effective_date": "2025-01-01",
                    "begin_date": "2025-01-01",
                    "end_date": None,  # older end_date is null
                    "updated_at": "2025-01-01T00:00:00",
                },
                {
                    "id": "cfg-new-expired",
                    "port_code": "PORT_A",
                    "port_name": "组合A",
                    "effective_date": "2026-01-01",
                    "begin_date": "2026-01-01",
                    "end_date": "2026-06-30",  # expired as of 2026-10-12
                    "updated_at": "2026-01-01T00:00:00",
                },
            ],
            "details": [
                {"id": "d-old", "config_id": "cfg-old", "index_code": "F_ALPHA", "index_name": "Alpha", "index_type": "core"},
                {"id": "d-new", "config_id": "cfg-new-expired", "index_code": "F_ALPHA", "index_name": "Alpha", "index_type": "core"},
            ],
        }
        snap_path, map_path = _create_isolated_env(tmp_path, snap_data)

        resolver = ReferencePortfolioResolver(snapshot_path=snap_path, mapping_path=map_path, as_of_date="2026-10-12")
        # cfg-new-expired superseded cfg-old, but cfg-new-expired is now expired.
        # Older cfg-old MUST NOT reappear!
        assert resolver.resolve("Alpha") == []


def test_effective_boundaries_and_missing_dates():
    """Boundary test: future dates excluded, inclusive end_date, missing effective_date excluded."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        snap_data = {
            "schema_version": 1,
            "exported_at": "2026-10-12T00:00:00Z",
            "configs": [
                {
                    "id": "cfg-future",
                    "port_code": "P_FUTURE",
                    "port_name": "未来生效",
                    "effective_date": "2026-12-01",
                    "begin_date": "2026-12-01",
                    "end_date": None,
                    "updated_at": "2026-01-01T00:00:00",
                },
                {
                    "id": "cfg-missing-date",
                    "port_code": "P_NODATE",
                    "port_name": "无日期",
                    "effective_date": None,  # missing date cannot silently current
                    "begin_date": None,
                    "end_date": None,
                    "updated_at": "2026-01-01T00:00:00",
                },
                {
                    "id": "cfg-exact-end",
                    "port_code": "P_EXACT",
                    "port_name": "今日截止",
                    "effective_date": "2026-01-01",
                    "begin_date": "2026-01-01",
                    "end_date": "2026-10-12",  # END_DATE inclusive: eligible today
                    "updated_at": "2026-01-01T00:00:00",
                },
            ],
            "details": [
                {"id": "d1", "config_id": "cfg-future", "index_code": "F_ALPHA", "index_name": "Alpha", "index_type": "core"},
                {"id": "d2", "config_id": "cfg-missing-date", "index_code": "F_ALPHA", "index_name": "Alpha", "index_type": "core"},
                {"id": "d3", "config_id": "cfg-exact-end", "index_code": "F_ALPHA", "index_name": "Alpha", "index_type": "core"},
            ],
        }
        snap_path, map_path = _create_isolated_env(tmp_path, snap_data)

        resolver = ReferencePortfolioResolver(snapshot_path=snap_path, mapping_path=map_path, as_of_date="2026-10-12")
        matches = resolver.resolve("Alpha")
        assert [m.port_code for m in matches] == ["P_EXACT"]


def test_deterministic_tie_breaking():
    """When effective_dates match, deterministic tie-breaking picks updated_at then ID."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        snap_data = {
            "schema_version": 1,
            "exported_at": "2026-10-12T00:00:00Z",
            "configs": [
                {
                    "id": "cfg-1",
                    "port_code": "P_TIE",
                    "port_name": "组合早期更新",
                    "effective_date": "2026-01-01",
                    "updated_at": "2026-01-01T10:00:00",
                },
                {
                    "id": "cfg-2",
                    "port_code": "P_TIE",
                    "port_name": "组合晚期更新",
                    "effective_date": "2026-01-01",
                    "updated_at": "2026-01-01T12:00:00",
                },
            ],
            "details": [
                {"id": "d1", "config_id": "cfg-1", "index_code": "F_ALPHA", "index_name": "Alpha 1", "index_type": "core"},
                {"id": "d2", "config_id": "cfg-2", "index_code": "F_ALPHA", "index_name": "Alpha 2", "index_type": "core"},
            ],
        }
        snap_path, map_path = _create_isolated_env(tmp_path, snap_data)

        resolver = ReferencePortfolioResolver(snapshot_path=snap_path, mapping_path=map_path, as_of_date="2026-10-12")
        matches = resolver.resolve("Alpha")
        assert len(matches) == 1
        assert matches[0].config_id == "cfg-2"
        assert matches[0].index_name == "Alpha 2"


def test_deduplication_and_stable_order():
    """Verify deduplication by port_code and stable ascending order by port_code."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        snap_data = {
            "schema_version": 1,
            "exported_at": "2026-10-12T00:00:00Z",
            "configs": [
                {"id": "c-z", "port_code": "Z99", "port_name": "Z组合", "effective_date": "2026-01-01"},
                {"id": "c-a", "port_code": "A01", "port_name": "A组合", "effective_date": "2026-01-01"},
                {"id": "c-m", "port_code": "M50", "port_name": "M组合", "effective_date": "2026-01-01"},
                # duplicate port_code in an older historical config
                {"id": "c-a-old", "port_code": "A01", "port_name": "A组合旧版", "effective_date": "2025-01-01"},
            ],
            "details": [
                {"id": "d1", "config_id": "c-z", "index_code": "F_ALPHA", "index_name": "Alpha", "index_type": "core"},
                {"id": "d2", "config_id": "c-a", "index_code": "F_ALPHA", "index_name": "Alpha", "index_type": "core"},
                {"id": "d3", "config_id": "c-m", "index_code": "F_ALPHA", "index_name": "Alpha", "index_type": "core"},
                {"id": "d4", "config_id": "c-a-old", "index_code": "F_ALPHA", "index_name": "Alpha 旧", "index_type": "core"},
            ],
        }
        snap_path, map_path = _create_isolated_env(tmp_path, snap_data)

        resolver = ReferencePortfolioResolver(snapshot_path=snap_path, mapping_path=map_path, as_of_date="2026-10-12")
        matches = resolver.resolve("Alpha")
        assert [m.port_code for m in matches] == ["A01", "M50", "Z99"]
        # A01 resolves to latest config c-a, not older c-a-old
        a_match = next(m for m in matches if m.port_code == "A01")
        assert a_match.config_id == "c-a"
