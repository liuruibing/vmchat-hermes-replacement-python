import pytest
from app.validation.validate_vm_report_dsl import validate_vm_report_dsl_set, ValidateOptions
from app.contracts.types import ValidationSuccess, ValidationFailure


def test_valid_create_dsl():
    valid_create_dsl = {
        "action": "create",
        "id": "3d1d1f05-7f55-46eb-8e5f-155018a7b97a",
        "requests": [{"id": "req1", "moduleId": "modA", "sqlCode": "3d1d1f05-7f55-46eb-8e5f-155018a7b97a"}],
        "transform": {
            "language": "javascript",
            "function": "function transform(responses) { return [{ c1: responses.req1 }]; }",
        },
        "view": {"type": "table", "title": "测试表", "columns": [{"field": "c1", "label": "L1"}]},
    }

    res = validate_vm_report_dsl_set(valid_create_dsl)
    assert res.ok is True
    assert isinstance(res, ValidationSuccess)
    assert len(res.dsls) == 1


def test_missing_request_reference():
    positional_dsl = {
        "action": "create",
        "id": "3d1d1f05-7f55-46eb-8e5f-155018a7b97a",
        "requests": [{"id": "req1", "moduleId": "modA", "sqlCode": "code1"}],
        "transform": {
            "language": "javascript",
            "function": "function transform(responses) { return [{ col1: responses[0] }]; }",
        },
        "view": {"type": "table", "columns": [{"field": "col1"}]},
    }

    res = validate_vm_report_dsl_set(positional_dsl)
    assert res.ok is False
    assert isinstance(res, ValidationFailure)
    assert any(e.code == "MISSING_REQUEST_REFERENCE" for e in res.errors)


def test_current_block_ids_single_update():
    uuid_100 = "00000000-0000-1000-8000-000000000100"
    update_dsl = {
        "action": "update",
        "id": uuid_100,
        "requests": [{"id": "req1", "moduleId": "modA", "sqlCode": "code1"}],
        "transform": {
            "language": "javascript",
            "function": "function transform(responses) { return [{ c1: responses.req1 }]; }",
        },
        "view": {"type": "table", "columns": [{"field": "c1"}]},
    }

    res_valid = validate_vm_report_dsl_set(update_dsl, options={"currentBlockIds": [uuid_100, "b-200"]})
    assert res_valid.ok is True

    res_invalid = validate_vm_report_dsl_set(update_dsl, options={"currentBlockIds": ["b-999"]})
    assert res_invalid.ok is False
    assert any(e.code == "UPDATE_TARGET_NOT_FOUND" for e in res_invalid.errors)


def test_batch_update_validations():
    uuid_1 = "00000000-0000-1000-8000-000000000001"
    uuid_2 = "00000000-0000-1000-8000-000000000002"
    uuid_3 = "00000000-0000-1000-8000-000000000003"
    dsl1 = {
        "action": "update",
        "id": uuid_1,
        "requests": [{"id": "req1", "moduleId": "modA", "sqlCode": "code1"}],
        "transform": {
            "language": "javascript",
            "function": "function transform(responses) { return [{ c1: responses.req1 }]; }",
        },
        "view": {"type": "table", "columns": [{"field": "c1"}]},
    }
    dsl2 = {
        "action": "update",
        "id": uuid_2,
        "requests": [{"id": "req1", "moduleId": "modA", "sqlCode": "code1"}],
        "transform": {
            "language": "javascript",
            "function": "function transform(responses) { return [{ c1: responses.req1 }]; }",
        },
        "view": {"type": "table", "columns": [{"field": "c1"}]},
    }

    # Valid batch
    res_batch = validate_vm_report_dsl_set([dsl1, dsl2], current_block_ids=[uuid_1, uuid_2, uuid_3])
    assert res_batch.ok is True

    # Duplicate target ID
    res_dup = validate_vm_report_dsl_set([dsl1, dsl1], current_block_ids=[uuid_1, uuid_2])
    assert res_dup.ok is False
    assert any(e.code == "BATCH_DUPLICATE_TARGET" for e in res_dup.errors)

    # Extra target not in currentBlockIds
    res_extra = validate_vm_report_dsl_set([dsl1, dsl2], current_block_ids=[uuid_1])
    assert res_extra.ok is False
    assert any(e.code == "BATCH_EXTRA_TARGET" for e in res_extra.errors)


def test_forbidden_tokens():
    forbidden_dsl = {
        "action": "create",
        "id": "3d1d1f05-7f55-46eb-8e5f-155018a7b97a",
        "requests": [{"id": "req1", "moduleId": "modA", "sqlCode": "code1"}],
        "transform": {
            "language": "javascript",
            "function": "function transform(responses) { window.alert('bad'); return [{ c1: responses.req1 }]; }",
        },
        "view": {"type": "table", "columns": [{"field": "c1"}]},
    }

    res = validate_vm_report_dsl_set(forbidden_dsl)
    assert res.ok is False
    assert any(e.code == "FORBIDDEN_IDENTIFIER" for e in res.errors)


def test_echarts_validation():
    echarts_dsl = {
        "action": "create",
        "id": "3d1d1f05-7f55-46eb-8e5f-155018a7b97a",
        "requests": [{"id": "req1", "moduleId": "modA", "sqlCode": "code1"}],
        "transform": {
            "language": "javascript",
            "function": "function transform(responses) { return [{ date: responses.req1, val: 10 }]; }",
        },
        "view": {
            "type": "echarts",
            "legend": {"show": True, "data": ["Series A"]},
            "dataset": {"source": "$transform", "dimensions": ["date", "val"]},
            "series": [
                {
                    "name": "Series A",
                    "type": "line",
                    "encode": {"x": "date", "y": "val"},
                }
            ],
            "xAxis": {"type": "category"},
            "yAxis": [{"type": "value"}],
        },
    }

    res = validate_vm_report_dsl_set(echarts_dsl)
    assert res.ok is True


def _cross_module_dsl(transform_function):
    return {
        "action": "create",
        "id": "3d1d1f05-7f55-46eb-8e5f-155018a7b97a",
        "requests": [
            {"id": "reqA", "moduleId": "modA", "sqlCode": "codeA"},
            {"id": "reqB", "moduleId": "modB", "sqlCode": "codeB"},
        ],
        "transform": {
            "language": "javascript",
            "function": transform_function,
        },
        "view": {
            "type": "table",
            "title": "跨模块",
            "columns": [
                {"field": "date", "label": "日期"},
                {"field": "a", "label": "A"},
                {"field": "b", "label": "B"},
            ],
        },
    }


def _time_series_profiles(entity="fund"):
    return {
        "modA": {
            "entity": entity,
            "shape": "time_series",
            "grain": {"primaryCanonicalKeys": ["date"]},
            "joinKeys": [{"canonical": "date", "rawFields": ["TDATE"]}],
            "taxonomy": None,
        },
        "modB": {
            "entity": entity,
            "shape": "time_series",
            "grain": {"primaryCanonicalKeys": ["date"]},
            "joinKeys": [{"canonical": "date", "rawFields": ["D_DATE"]}],
            "taxonomy": None,
        },
    }


def test_cross_module_semantic_validation_accepts_explicit_shared_grain():
    dsl = _cross_module_dsl(
        "function transform(responses) { "
        "var x = responses.reqA && responses.reqA.TDATE; "
        "var y = responses.reqB && responses.reqB.D_DATE; "
        "return [{ date: x || y, a: 1, b: 2 }]; }"
    )

    res = validate_vm_report_dsl_set(
        dsl,
        options={"moduleProfiles": _time_series_profiles()},
    )

    assert res.ok is True


def test_cross_module_semantic_validation_rejects_unknown_entity():
    dsl = _cross_module_dsl(
        "function transform(responses) { "
        "var x = responses.reqA && responses.reqA.TDATE; "
        "var y = responses.reqB && responses.reqB.D_DATE; "
        "return [{ date: x || y, a: 1, b: 2 }]; }"
    )

    res = validate_vm_report_dsl_set(
        dsl,
        options={"moduleProfiles": _time_series_profiles(entity="unknown")},
    )

    assert res.ok is False
    assert any(e.code == "SEMANTIC_ENTITY_UNPROVEN" for e in res.errors)


def test_cross_module_semantic_validation_rejects_unreferenced_join_key():
    dsl = _cross_module_dsl(
        "function transform(responses) { "
        "var x = responses.reqA; var y = responses.reqB; "
        "return [{ date: '20260101', a: x.value, b: y.value }]; }"
    )

    res = validate_vm_report_dsl_set(
        dsl,
        options={"moduleProfiles": _time_series_profiles()},
    )

    assert res.ok is False
    assert any(e.code == "SEMANTIC_JOIN_KEY_NOT_USED" for e in res.errors)


def test_cross_module_semantic_validation_rejects_taxonomy_mismatch():
    profiles = {
        "modA": {
            "entity": "fund",
            "shape": "cross_section",
            "grain": {"primaryCanonicalKeys": ["industry"]},
            "joinKeys": [{"canonical": "industry", "rawFields": ["industryCode"]}],
            "taxonomy": "SWSR",
        },
        "modB": {
            "entity": "fund",
            "shape": "cross_section",
            "grain": {"primaryCanonicalKeys": ["industry"]},
            "joinKeys": [{"canonical": "industry", "rawFields": ["industryCode"]}],
            "taxonomy": "HS_CUSTOM",
        },
    }
    dsl = _cross_module_dsl(
        "function transform(responses) { "
        "var x = responses.reqA && responses.reqA.industryCode; "
        "var y = responses.reqB && responses.reqB.industryCode; "
        "return [{ date: x || y, a: 1, b: 2 }]; }"
    )

    res = validate_vm_report_dsl_set(dsl, options={"moduleProfiles": profiles})

    assert res.ok is False
    assert any(e.code == "SEMANTIC_TAXONOMY_MISMATCH" for e in res.errors)
