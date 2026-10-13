from __future__ import annotations

import hashlib
import json
import pytest
import concurrent.futures
from pathlib import Path
from pydantic import ValidationError

from app.mandate_risk.catalogue import (
    compile_catalogue,
    generate_canonical_markdown_content,
    get_default_artifact_path,
    get_default_markdown_path,
    load_prebuilt_registry,
    main,
    parse_markdown_catalogue,
)
from app.mandate_risk.models import RawRiskMetric
from app.mandate_risk.registry import RawRiskMetricRegistry, _build_rows, _read_csv_values

RAW_CSV_PATH = (
    Path(__file__).resolve().parents[1]
    / "agents"
    / "mandate_risk_ai"
    / "knowledge"
    / "raw"
    / "risk_metrics.raw.csv"
)


def test_catalogue_preservation():
    """Verify 100% parity between original raw CSV rows and generated JSON registry."""
    raw_rows = _build_rows(_read_csv_values(RAW_CSV_PATH))

    registry = load_prebuilt_registry()
    metrics = registry.all()

    assert len(metrics) == 34
    assert len(raw_rows) == 34

    for raw, loaded in zip(raw_rows, metrics):
        assert loaded.model_dump() == raw.model_dump()


def test_catalogue_edits_affect_generated(tmp_path: Path):
    """Test editing a field in Markdown updates the generated JSON artifact upon compilation."""
    raw_rows = _build_rows(_read_csv_values(RAW_CSV_PATH))

    modified_rows = [r.model_copy() for r in raw_rows]
    modified_rows[0] = RawRiskMetric(
        row_id=2,
        source_row=2,
        raw_risk_type_1="收益风险（6）",
        raw_risk_type_2="收益率",
        metric_name="基金收益率",
        algorithm="MODIFIED_ALGORITHM_FORMULA",
        mandate="MODIFIED_MANDATE_TEXT",
        strategy_type="权益/固收",
        effective_risk_type_1="收益风险（6）",
        effective_risk_type_2="收益率",
    )

    md_path = tmp_path / "指标知识库.md"
    json_path = tmp_path / "指标知识库.generated.json"

    md_content = generate_canonical_markdown_content(modified_rows)
    md_path.write_text(md_content, encoding="utf-8")

    payload = compile_catalogue(md_path, json_path)
    assert payload["metrics"][0]["algorithm"] == "MODIFIED_ALGORITHM_FORMULA"
    assert payload["metrics"][0]["mandate"] == "MODIFIED_MANDATE_TEXT"

    registry = load_prebuilt_registry(json_path)
    metric = registry.get(2)
    assert metric is not None
    assert metric.algorithm == "MODIFIED_ALGORITHM_FORMULA"
    assert metric.mandate == "MODIFIED_MANDATE_TEXT"


def test_catalogue_changed_source_stale_rejection(tmp_path: Path):
    """Test modifying Markdown source without recompiling JSON causes load_prebuilt_registry to fail with actionable error."""
    raw_rows = _build_rows(_read_csv_values(RAW_CSV_PATH))

    md_path = tmp_path / "指标知识库.md"
    json_path = tmp_path / "指标知识库.generated.json"

    md_content = generate_canonical_markdown_content(raw_rows)
    md_path.write_text(md_content, encoding="utf-8")
    compile_catalogue(md_path, json_path)

    # Verify check passes before source edit
    compile_catalogue(md_path, json_path, check_only=True)

    # Modify Markdown source file
    md_path.write_text(md_content + "\n<!-- modification -->\n", encoding="utf-8")

    with pytest.raises(ValueError, match="STALE_PREBUILT_REGISTRY"):
        load_prebuilt_registry(json_path)

    with pytest.raises(ValueError, match="STALE_PREBUILT_REGISTRY"):
        compile_catalogue(md_path, json_path, check_only=True)


def test_catalogue_duplicate_id_and_name_failures():
    """Test duplicate row_id or duplicate metric_name fails parsing/compilation."""
    raw_rows = _build_rows(_read_csv_values(RAW_CSV_PATH))

    # Duplicate row_id
    dup_id_rows = [r.model_copy() for r in raw_rows]
    dup_id_rows[1] = RawRiskMetric(
        row_id=2,  # duplicate ID
        source_row=3,
        raw_risk_type_1="",
        raw_risk_type_2="",
        metric_name="超额收益率（基准超额）",
        algorithm="Ri- Bi",
        mandate="test",
        strategy_type="权益/固收",
        effective_risk_type_1="收益风险（6）",
        effective_risk_type_2="收益率",
    )
    dup_id_md = generate_canonical_markdown_content(dup_id_rows)
    with pytest.raises(ValueError, match="DUPLICATE_RISK_METRIC_ROW_ID"):
        parse_markdown_catalogue(dup_id_md)

    # Duplicate metric_name
    dup_name_rows = [r.model_copy() for r in raw_rows]
    dup_name_rows[1] = RawRiskMetric(
        row_id=3,
        source_row=3,
        raw_risk_type_1="",
        raw_risk_type_2="",
        metric_name="基金收益率",  # duplicate name with row_id=2
        algorithm="Ri- Bi",
        mandate="test",
        strategy_type="权益/固收",
        effective_risk_type_1="收益风险（6）",
        effective_risk_type_2="收益率",
    )
    dup_name_md = generate_canonical_markdown_content(dup_name_rows)
    with pytest.raises(ValueError, match="DUPLICATE_RISK_METRIC_NAME"):
        parse_markdown_catalogue(dup_name_md)


def test_catalogue_no_overwrite_on_invalid_source(tmp_path: Path):
    """Test compiling invalid Markdown source fails and does NOT overwrite existing valid JSON artifact."""
    raw_rows = _build_rows(_read_csv_values(RAW_CSV_PATH))

    md_path = tmp_path / "指标知识库.md"
    json_path = tmp_path / "指标知识库.generated.json"

    # Write initial valid content
    md_path.write_text(generate_canonical_markdown_content(raw_rows), encoding="utf-8")
    compile_catalogue(md_path, json_path)

    original_json_bytes = json_path.read_bytes()

    # Create invalid markdown content (missing required field)
    invalid_md = (
        "# Header\n\n"
        "## [ID: 2] Invalid Metric\n"
        "- **row_id**: 2\n"
        "- **source_row**: 2\n"
        "- **metric_name**: Invalid Metric\n"
        # missing other required fields
    )
    bad_md_path = tmp_path / "bad.md"
    bad_md_path.write_text(invalid_md, encoding="utf-8")

    with pytest.raises(ValueError, match="MISSING_MARKDOWN_FIELD"):
        compile_catalogue(bad_md_path, json_path)

    # Verify json_path content was completely untouched
    assert json_path.read_bytes() == original_json_bytes


def test_catalogue_unrecognized_markdown_content_rejection():
    """Test that arbitrary unrecognized nonblank lines inside metric section raise ValueError."""
    bad_md = (
        "# Header\n\n"
        "## [ID: 2] Test Metric\n"
        "- **row_id**: 2\n"
        "- **source_row**: 2\n"
        "some random unparsed content line here\n"
        "- **raw_risk_type_1**: test\n"
    )
    with pytest.raises(ValueError, match="UNRECOGNIZED_MARKDOWN_CONTENT"):
        parse_markdown_catalogue(bad_md)


@pytest.mark.parametrize(
    ("old_heading", "new_heading"),
    [
        ("## [ID: 2] 基金收益率", "## [ID: 2] 修改后的名称"),
        ("## [ID: 2] 基金收益率", "## [ID: 200] 基金收益率"),
    ],
)
def test_catalogue_rejects_heading_only_business_edits(old_heading, new_heading):
    rows = _build_rows(_read_csv_values(RAW_CSV_PATH))
    content = generate_canonical_markdown_content(rows).replace(old_heading, new_heading, 1)
    with pytest.raises(ValueError, match="INCONSISTENT_MARKDOWN_HEADING"):
        parse_markdown_catalogue(content)


def test_catalogue_multiline_text_roundtrip():
    """Test multiline algorithm (like VaR's 9 lines) and mandate texts roundtrip without text loss."""
    raw_rows = _build_rows(_read_csv_values(RAW_CSV_PATH))

    var_metric = next(r for r in raw_rows if r.metric_name == "VaR")
    assert "\n" in var_metric.algorithm
    algorithm_lines = var_metric.algorithm.split("\n")

    md_content = generate_canonical_markdown_content(raw_rows)
    parsed = parse_markdown_catalogue(md_content)

    parsed_var = next(r for r in parsed if r.metric_name == "VaR")
    assert parsed_var.algorithm == var_metric.algorithm
    assert parsed_var.algorithm.split("\n") == algorithm_lines


def test_catalogue_determinism(tmp_path: Path):
    """Test compiling the same Markdown source multiple times produces identical byte-for-byte JSON output."""
    raw_rows = _build_rows(_read_csv_values(RAW_CSV_PATH))

    md_path = tmp_path / "指标知识库.md"
    json_1 = tmp_path / "out1.generated.json"
    json_2 = tmp_path / "out2.generated.json"

    md_path.write_text(generate_canonical_markdown_content(raw_rows), encoding="utf-8")

    compile_catalogue(md_path, json_1)
    compile_catalogue(md_path, json_2)

    assert json_1.read_bytes() == json_2.read_bytes()


def test_catalogue_runtime_non_json_rejection(tmp_path: Path):
    """Test load_prebuilt_registry rejects non-JSON inputs at runtime."""
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("a,b,c\n", encoding="utf-8")

    xlsx_file = tmp_path / "test.xlsx"
    xlsx_file.write_bytes(b"dummy")

    with pytest.raises(ValueError, match="INVALID_PREBUILT_REGISTRY_FORMAT"):
        load_prebuilt_registry(csv_file)

    with pytest.raises(ValueError, match="INVALID_PREBUILT_REGISTRY_FORMAT"):
        load_prebuilt_registry(xlsx_file)


def test_catalogue_runtime_strict_schema_validation(tmp_path: Path):
    """Test strict JSON schema, version type, field exactness, and negative ID rejection."""
    md_path = tmp_path / "指标知识库.md"
    md_path.write_text("# Header\n\n## [ID: 2] Metric\n", encoding="utf-8")
    md_hash = hashlib.sha256(md_path.read_bytes()).hexdigest()

    valid_dict = {
        "version": 1,
        "source": {"path": "指标知识库.md", "sha256": md_hash, "sheet": "风险指标库"},
        "metrics": [
            {
                "row_id": 2,
                "source_row": 2,
                "raw_risk_type_1": "type1",
                "raw_risk_type_2": "type2",
                "effective_risk_type_1": "type1",
                "effective_risk_type_2": "type2",
                "strategy_type": "strat",
                "metric_name": "name",
                "algorithm": "algo",
                "mandate": "mandate",
            }
        ],
    }

    # Version = True (bool) rejection
    bad_v_dict = dict(valid_dict, version=True)
    json_path = tmp_path / "bad_v.json"
    json_path.write_text(json.dumps(bad_v_dict), encoding="utf-8")
    with pytest.raises(ValueError, match="UNSUPPORTED_PREBUILT_REGISTRY_VERSION"):
        load_prebuilt_registry(json_path)

    # Negative row_id rejection
    bad_id_dict = json.loads(json.dumps(valid_dict))
    bad_id_dict["metrics"][0]["row_id"] = -1
    json_path_id = tmp_path / "bad_id.json"
    json_path_id.write_text(json.dumps(bad_id_dict), encoding="utf-8")
    with pytest.raises(ValueError, match="INVALID_PREBUILT_REGISTRY_METRIC"):
        load_prebuilt_registry(json_path_id)

    # Extra unknown metric field rejection
    bad_extra_dict = json.loads(json.dumps(valid_dict))
    bad_extra_dict["metrics"][0]["extra_unknown_key"] = "bad"
    json_path_extra = tmp_path / "bad_extra.json"
    json_path_extra.write_text(json.dumps(bad_extra_dict), encoding="utf-8")
    with pytest.raises(ValueError, match="INVALID_PREBUILT_REGISTRY_METRIC"):
        load_prebuilt_registry(json_path_extra)


def test_catalogue_business_edit_effective_risk_type(tmp_path: Path):
    """Test business edits to explicit effective risk classifications compile and load as authoritative."""
    raw_rows = _build_rows(_read_csv_values(RAW_CSV_PATH))

    modified_rows = [r.model_copy() for r in raw_rows]
    # Explicitly edit effective risk type on row 3 without altering raw fields or neighbors
    modified_rows[1] = RawRiskMetric(
        row_id=3,
        source_row=3,
        raw_risk_type_1="",
        raw_risk_type_2="",
        metric_name="超额收益率（基准超额）",
        algorithm="Ri- Bi",
        mandate="test",
        strategy_type="权益/固收",
        effective_risk_type_1="自定义业务一级分类",
        effective_risk_type_2="自定义业务二级分类",
    )

    md_path = tmp_path / "指标知识库.md"
    json_path = tmp_path / "指标知识库.generated.json"

    md_content = generate_canonical_markdown_content(modified_rows)
    md_path.write_text(md_content, encoding="utf-8")

    compile_catalogue(md_path, json_path)

    reg = load_prebuilt_registry(json_path)
    loaded_metric = reg.require(3)

    assert loaded_metric.effective_risk_type_1 == "自定义业务一级分类"
    assert loaded_metric.effective_risk_type_2 == "自定义业务二级分类"
    # Provenance raw fields remain empty string as authored
    assert loaded_metric.raw_risk_type_1 == ""
    assert loaded_metric.raw_risk_type_2 == ""


def test_catalogue_section_reorder_preservation(tmp_path: Path):
    """Test reordering metric sections in Markdown preserves IDs, source_row, and effective risk classifications."""
    raw_rows = _build_rows(_read_csv_values(RAW_CSV_PATH))

    reordered_rows = list(reversed(raw_rows))

    md_path = tmp_path / "reordered.md"
    json_path = tmp_path / "reordered.json"

    md_path.write_text(generate_canonical_markdown_content(reordered_rows), encoding="utf-8")

    compile_catalogue(md_path, json_path)
    registry = load_prebuilt_registry(json_path)

    for orig in raw_rows:
        loaded = registry.require(orig.row_id)
        assert loaded.source_row == orig.source_row
        assert loaded.effective_risk_type_1 == orig.effective_risk_type_1
        assert loaded.effective_risk_type_2 == orig.effective_risk_type_2


def test_catalogue_concurrent_compilation(tmp_path: Path):
    """Test concurrent compilation to same output artifact directory operates safely."""
    raw_rows = _build_rows(_read_csv_values(RAW_CSV_PATH))

    md_path = tmp_path / "指标知识库.md"
    json_path = tmp_path / "指标知识库.generated.json"

    md_path.write_text(generate_canonical_markdown_content(raw_rows), encoding="utf-8")

    def run_compile():
        return compile_catalogue(md_path, json_path)

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(run_compile) for _ in range(10)]
        for future in futures:
            future.result()

    loaded_rows = load_prebuilt_registry(json_path).all()
    assert [row.model_dump() for row in loaded_rows] == [
        row.model_dump() for row in raw_rows
    ]


def test_catalogue_cli(tmp_path: Path):
    """Test python -m app.mandate_risk.catalogue CLI --check and compilation."""
    raw_rows = _build_rows(_read_csv_values(RAW_CSV_PATH))

    md_path = tmp_path / "指标知识库.md"
    json_path = tmp_path / "指标知识库.generated.json"

    md_path.write_text(generate_canonical_markdown_content(raw_rows), encoding="utf-8")

    # Compile via CLI args
    exit_code = main(["--source", str(md_path), "--output", str(json_path)])
    assert exit_code == 0
    assert json_path.exists()

    # Check via CLI args
    check_code = main(["--check", "--source", str(md_path), "--output", str(json_path)])
    assert check_code == 0

    original_artifact = json_path.read_bytes()
    md_path.write_text(
        md_path.read_text(encoding="utf-8").replace(
            "- **algorithm**: Ri- Bi", "- **algorithm**: modified algorithm", 1
        ),
        encoding="utf-8",
    )
    assert main(["--check", "--source", str(md_path), "--output", str(json_path)]) == 1
    assert json_path.read_bytes() == original_artifact


@pytest.mark.parametrize("invalid_version", [True, 1.0])
def test_catalogue_check_rejects_numeric_schema_coercions(tmp_path, invalid_version):
    rows = _build_rows(_read_csv_values(RAW_CSV_PATH))
    source, output = tmp_path / "source.md", tmp_path / "output.json"
    source.write_text(generate_canonical_markdown_content(rows), encoding="utf-8")
    payload = compile_catalogue(source, output)
    payload["version"] = invalid_version
    output.write_text(json.dumps(payload), encoding="utf-8")
    original_artifact = output.read_bytes()

    assert main(["--check", "--source", str(source), "--output", str(output)]) == 1
    assert output.read_bytes() == original_artifact


def test_raw_metric_frozen_immutability():
    """Test that RawRiskMetric objects are immutable (frozen)."""
    raw_rows = _build_rows(_read_csv_values(RAW_CSV_PATH))
    metric = raw_rows[0]
    original_name = metric.metric_name

    with pytest.raises(ValidationError) as exc_info:
        metric.metric_name = "MutatedName"

    assert exc_info.value.errors()[0]["type"] == "frozen_instance"
    assert metric.metric_name == original_name
