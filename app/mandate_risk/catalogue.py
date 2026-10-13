from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from app.mandate_risk.models import RawRiskMetric
from app.mandate_risk.registry import RawRiskMetricRegistry

DEFAULT_CANONICAL_MD_NAME = "指标知识库.md"
DEFAULT_GENERATED_JSON_NAME = "指标知识库.generated.json"
SCHEMA_VERSION = 1
DEFAULT_SHEET_NAME = "风险指标库"

REQUIRED_FIELDS = [
    "row_id",
    "source_row",
    "raw_risk_type_1",
    "raw_risk_type_2",
    "effective_risk_type_1",
    "effective_risk_type_2",
    "strategy_type",
    "metric_name",
    "algorithm",
    "mandate",
]


def get_repo_root() -> Path:
    """Return the repository root directory."""
    return Path(__file__).resolve().parents[2]


def get_default_markdown_path() -> Path:
    """Return default canonical Markdown path."""
    return get_repo_root() / DEFAULT_CANONICAL_MD_NAME


def get_default_artifact_path() -> Path:
    """Return default prebuilt JSON artifact path."""
    return get_repo_root() / DEFAULT_GENERATED_JSON_NAME


def format_field_to_markdown(name: str, value: str) -> List[str]:
    """Format a single field for Markdown section output.

    Uses fenced code blocks when strings contain newlines, leading spaces,
    or trailing spaces to preserve string fidelity.
    """
    val = value or ""
    if "\n" in val or val.startswith(" ") or val.endswith(" "):
        lines = [f"- **{name}**:"]
        lines.append("```")
        lines.extend(val.split("\n"))
        lines.append("```")
        return lines
    return [f"- **{name}**: {val}"]


def format_metric_to_markdown(metric: RawRiskMetric) -> str:
    """Serialize a single RawRiskMetric to Markdown section format."""
    lines = [f"## [ID: {metric.row_id}] {metric.metric_name}", ""]
    lines.extend(format_field_to_markdown("row_id", str(metric.row_id)))
    lines.extend(format_field_to_markdown("source_row", str(metric.source_row)))
    lines.extend(format_field_to_markdown("raw_risk_type_1", metric.raw_risk_type_1))
    lines.extend(format_field_to_markdown("raw_risk_type_2", metric.raw_risk_type_2))
    lines.extend(
        format_field_to_markdown("effective_risk_type_1", metric.effective_risk_type_1)
    )
    lines.extend(
        format_field_to_markdown("effective_risk_type_2", metric.effective_risk_type_2)
    )
    lines.extend(format_field_to_markdown("strategy_type", metric.strategy_type))
    lines.extend(format_field_to_markdown("metric_name", metric.metric_name))
    lines.extend(format_field_to_markdown("algorithm", metric.algorithm))
    lines.extend(format_field_to_markdown("mandate", metric.mandate))
    return "\n".join(lines)


def generate_canonical_markdown_content(
    metrics: List[RawRiskMetric],
    csv_sha256: str = "cd097edb49be7b73152292722db71d41e7f65d40444b35cd7fc3e96a071fc4d5",
) -> str:
    """Generate the full canonical Markdown file content with maintenance prose."""
    header_parts = [
        "# 风险指标知识库",
        "",
        "> **维护说明**：",
        "> 1. 本 Markdown 文件为风险指标知识库唯一的人工维护事实源。",
        "> 2. 禁止直接修改 `指标知识库.generated.json`。修改本文件后，必须运行 CLI 工具重新编译生成 JSON 产物：",
        ">    `python -m app.mandate_risk.catalogue`",
        "> 3. 校验产物状态（不写入）：`python -m app.mandate_risk.catalogue --check`",
        "> 4. 新增或修改指标模板：",
        "> ```markdown",
        "> ## [ID: 36] 指标名称",
        "> - **row_id**: 36",
        "> - **source_row**: 36",
        "> - **raw_risk_type_1**: 原始一级分类",
        "> - **raw_risk_type_2**: 原始二级分类",
        "> - **effective_risk_type_1**: 有效一级分类",
        "> - **effective_risk_type_2**: 有效二级分类",
        "> - **strategy_type**: 适用策略",
        "> - **metric_name**: 指标名称",
        "> - **algorithm**: 指标算法",
        "> - **mandate**: Mandate字段",
        "> ```",
        "> 5. 归档来源：`agents/mandate_risk_ai/knowledge/raw/risk_metrics.raw.csv`",
        f"> 6. 归档文件 SHA-256：`{csv_sha256}`",
        "",
        "---",
        "",
    ]
    body = "\n\n".join(format_metric_to_markdown(m) for m in metrics)
    return "\n".join(header_parts) + body + "\n"


def parse_markdown_catalogue(content: str) -> List[RawRiskMetric]:
    """Parse canonical Markdown catalogue content into RawRiskMetric objects.

    Strictly validates metric sections: rejects unrecognized nonblank content,
    validates duplicate/missing fields, integer IDs, and unique names/IDs.
    Effective classifications are authoritative as explicit fields.
    """
    lines = content.splitlines()
    i = 0
    raw_sections: List[Tuple[str, Dict[str, str]]] = []

    while i < len(lines):
        line = lines[i]
        if line.startswith("## "):
            heading = line.strip()
            i += 1
            fields: Dict[str, str] = {}
            seen_keys: Set[str] = set()

            while i < len(lines) and not lines[i].startswith("## "):
                curr = lines[i]
                stripped = curr.strip()

                # Allow blank lines or documented comment lines/separators inside metric section
                if not stripped or stripped.startswith("<!--") or stripped.startswith("//") or stripped.startswith(">"):
                    i += 1
                    continue

                if curr.startswith("- **"):
                    match = re.match(
                        r"^-\s*\*\*([a-zA-Z0-9_]+)\*\*:(?: (.*))?$", curr
                    )
                    if not match:
                        raise ValueError(
                            f"MALFORMED_MARKDOWN_FIELD: Invalid field syntax '{curr}' in section '{heading}'"
                        )
                    key = match.group(1)
                    if key in seen_keys:
                        raise ValueError(
                            f"DUPLICATE_MARKDOWN_FIELD: Field '{key}' duplicated in section '{heading}'"
                        )
                    if key not in REQUIRED_FIELDS:
                        raise ValueError(
                            f"UNKNOWN_MARKDOWN_FIELD: Field '{key}' is not recognized in section '{heading}'"
                        )

                    seen_keys.add(key)
                    v = match.group(2)
                    if v is None or v == "":
                        # Check if next line starts a code fence
                        if i + 1 < len(lines) and lines[i + 1].startswith("```"):
                            i += 2
                            fence_lines: List[str] = []
                            while i < len(lines) and not lines[i].startswith("```"):
                                fence_lines.append(lines[i])
                                i += 1
                            if i >= len(lines):
                                raise ValueError(
                                    f"MALFORMED_MARKDOWN_SECTION: Unclosed code block in field '{key}' of section '{heading}'"
                                )
                            v = "\n".join(fence_lines)
                    fields[key] = v if v is not None else ""
                    i += 1
                else:
                    raise ValueError(
                        f"UNRECOGNIZED_MARKDOWN_CONTENT: Unrecognized content line '{curr}' in section '{heading}'. "
                        f"All section contents must be valid field entries, code blocks, or comments."
                    )
            raw_sections.append((heading, fields))
        else:
            i += 1

    if not raw_sections:
        raise ValueError("EMPTY_RISK_METRIC_SOURCE: No metric sections found in Markdown source")

    metrics: List[RawRiskMetric] = []
    seen_ids: Set[int] = set()
    seen_names: Set[str] = set()

    for heading, fields in raw_sections:
        missing = [f for f in REQUIRED_FIELDS if f not in fields]
        if missing:
            raise ValueError(
                f"MISSING_MARKDOWN_FIELD: Section '{heading}' missing required fields: {', '.join(missing)}"
            )

        try:
            row_id = int(fields["row_id"])
            if row_id <= 0:
                raise ValueError()
        except Exception:
            raise ValueError(
                f"INVALID_MARKDOWN_INTEGER: Field 'row_id' in section '{heading}' must be a positive integer, got {fields['row_id']!r}"
            )

        try:
            source_row = int(fields["source_row"])
            if source_row <= 0:
                raise ValueError()
        except Exception:
            raise ValueError(
                f"INVALID_MARKDOWN_INTEGER: Field 'source_row' in section '{heading}' must be a positive integer, got {fields['source_row']!r}"
            )

        metric_name = fields["metric_name"].strip()
        if not metric_name:
            raise ValueError(f"EMPTY_METRIC_NAME: Metric name empty in section '{heading}'")

        heading_match = re.fullmatch(r"## \[ID: ([1-9]\d*)\] (.+)", heading)
        if (
            heading_match is None
            or int(heading_match.group(1)) != row_id
            or heading_match.group(2) != metric_name
        ):
            raise ValueError(
                f"INCONSISTENT_MARKDOWN_HEADING: Section '{heading}' must match "
                f"'## [ID: {row_id}] {metric_name}'. Update both the heading and its fields."
            )

        if row_id in seen_ids:
            raise ValueError(f"DUPLICATE_RISK_METRIC_ROW_ID: Duplicate row_id {row_id} in section '{heading}'")
        seen_ids.add(row_id)

        if metric_name in seen_names:
            raise ValueError(f"DUPLICATE_RISK_METRIC_NAME: Duplicate metric_name {metric_name!r} in section '{heading}'")
        seen_names.add(metric_name)

        metric = RawRiskMetric(
            row_id=row_id,
            source_row=source_row,
            raw_risk_type_1=fields["raw_risk_type_1"],
            raw_risk_type_2=fields["raw_risk_type_2"],
            metric_name=metric_name,
            algorithm=fields["algorithm"],
            mandate=fields["mandate"],
            strategy_type=fields["strategy_type"],
            effective_risk_type_1=fields["effective_risk_type_1"],
            effective_risk_type_2=fields["effective_risk_type_2"],
        )
        metrics.append(metric)

    return metrics


def compile_catalogue(
    source_path: str | Path,
    output_path: str | Path | None = None,
    *,
    check_only: bool = False,
) -> Dict[str, Any]:
    """Compile Markdown risk metric knowledge base into JSON artifact.

    Args:
        source_path: Path to canonical Markdown source (e.g. 指标知识库.md).
        output_path: Path to target JSON artifact (e.g. 指标知识库.generated.json).
            Defaults to source_path.parent / (source_path.stem + ".generated.json").
        check_only: If True, validate existing artifact up-to-date without writing.

    Returns:
        The compiled JSON dictionary payload.
    """
    src = Path(source_path).resolve()
    if not src.exists():
        raise FileNotFoundError(f"MARKDOWN_SOURCE_NOT_FOUND: Markdown source '{src}' does not exist.")

    md_bytes = src.read_bytes()
    md_sha256 = hashlib.sha256(md_bytes).hexdigest()
    md_content = md_bytes.decode("utf-8")

    metrics = parse_markdown_catalogue(md_content)

    if output_path is not None:
        out = Path(output_path).resolve()
    else:
        out = src.parent / f"{src.stem}.generated.json"

    rel_source_path = os.path.relpath(src, out.parent)

    payload: Dict[str, Any] = {
        "version": SCHEMA_VERSION,
        "source": {
            "path": rel_source_path,
            "sha256": md_sha256,
            "sheet": DEFAULT_SHEET_NAME,
        },
        "metrics": [m.model_dump() for m in metrics],
    }

    if check_only:
        if not out.exists():
            raise ValueError(
                f"STALE_PREBUILT_REGISTRY: Prebuilt artifact '{out}' does not exist. "
                f"Run 'python -m app.mandate_risk.catalogue' to generate it."
            )
        try:
            existing_payload = json.loads(out.read_text(encoding="utf-8"))
        except Exception as exc:
            raise ValueError(
                f"STALE_PREBUILT_REGISTRY: Artifact '{out}' contains invalid JSON ({exc}). "
                f"Run 'python -m app.mandate_risk.catalogue' to regenerate."
            ) from exc

        # Python equality conflates True, 1 and 1.0; JSON schema types must not.
        if json.dumps(existing_payload, sort_keys=True) != json.dumps(payload, sort_keys=True):
            raise ValueError(
                f"STALE_PREBUILT_REGISTRY: Artifact '{out}' is out of date relative to Markdown source '{src}'. "
                f"Run 'python -m app.mandate_risk.catalogue' to update."
            )
        return payload

    # Concurrent-safe atomic write using unique temporary file in output directory
    out.parent.mkdir(parents=True, exist_ok=True)
    formatted_json = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"

    fd, temp_path_str = tempfile.mkstemp(
        dir=out.parent,
        prefix=f".{out.name}.",
        suffix=".tmp",
    )
    temp_path = Path(temp_path_str)

    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(formatted_json)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, out)
    except Exception:
        if temp_path.exists():
            try:
                temp_path.unlink()
            except OSError:
                pass
        raise

    return payload


def load_prebuilt_registry(
    path: str | Path | None = None,
) -> RawRiskMetricRegistry:
    """Load prebuilt RawRiskMetricRegistry from prebuilt JSON artifact.

    Strictly validates root keys, version type/value, source path/sha256/sheet types,
    exact 10 metric fields, positive IDs, nonblank names, and Markdown SHA-256 freshness.
    Fails with actionable error if missing/stale/invalid. Never invokes Markdown parser or CSV fallback.
    """
    if path is None:
        env_val = os.environ.get("MANDATE_RISK_METRIC_SOURCE")
        if env_val and env_val.strip():
            target_path = Path(env_val.strip())
        else:
            target_path = get_default_artifact_path()
    else:
        target_path = Path(path)

    target_path = target_path.resolve()

    if target_path.suffix.lower() != ".json":
        raise ValueError(
            f"INVALID_PREBUILT_REGISTRY_FORMAT: Expected .json prebuilt artifact, got '{target_path.suffix}' "
            f"for '{target_path}'. Only prebuilt JSON artifacts are supported at runtime."
        )

    if not target_path.exists():
        raise ValueError(
            f"PREBUILT_REGISTRY_NOT_FOUND: Prebuilt artifact '{target_path}' not found. "
            f"Run 'python -m app.mandate_risk.catalogue' to generate it."
        )

    try:
        data = json.loads(target_path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ValueError(
            f"INVALID_PREBUILT_REGISTRY_JSON: Failed to parse prebuilt artifact JSON in '{target_path}': {exc}. "
            f"Run 'python -m app.mandate_risk.catalogue' to regenerate."
        ) from exc

    if not isinstance(data, dict):
        raise ValueError(
            f"INVALID_PREBUILT_REGISTRY_SCHEMA: Root in '{target_path}' must be a JSON object. "
            f"Run 'python -m app.mandate_risk.catalogue' to regenerate."
        )

    if set(data.keys()) != {"version", "source", "metrics"}:
        raise ValueError(
            f"INVALID_PREBUILT_REGISTRY_SCHEMA: Root keys in '{target_path}' must be exactly ['version', 'source', 'metrics']. "
            f"Run 'python -m app.mandate_risk.catalogue' to regenerate."
        )

    version = data.get("version")
    if isinstance(version, bool) or not isinstance(version, int) or version != SCHEMA_VERSION:
        raise ValueError(
            f"UNSUPPORTED_PREBUILT_REGISTRY_VERSION: Version {version!r} in '{target_path}' is invalid (expected integer {SCHEMA_VERSION}). "
            f"Run 'python -m app.mandate_risk.catalogue' to regenerate."
        )

    source_info = data.get("source")
    if not isinstance(source_info, dict) or set(source_info.keys()) != {"path", "sha256", "sheet"}:
        raise ValueError(
            f"INVALID_PREBUILT_REGISTRY_SCHEMA: 'source' in '{target_path}' must have keys ['path', 'sha256', 'sheet']. "
            f"Run 'python -m app.mandate_risk.catalogue' to regenerate."
        )

    source_rel_path = source_info.get("path")
    expected_sha256 = source_info.get("sha256")
    sheet_name = source_info.get("sheet")

    if not isinstance(source_rel_path, str) or not source_rel_path.strip():
        raise ValueError(f"INVALID_PREBUILT_REGISTRY_SCHEMA: Invalid 'source.path' in '{target_path}'.")
    if not isinstance(expected_sha256, str) or len(expected_sha256) != 64 or not re.match(r"^[0-9a-fA-F]{64}$", expected_sha256):
        raise ValueError(f"INVALID_PREBUILT_REGISTRY_SCHEMA: Invalid 'source.sha256' hex hash in '{target_path}'.")
    if not isinstance(sheet_name, str) or not sheet_name.strip():
        raise ValueError(f"INVALID_PREBUILT_REGISTRY_SCHEMA: Invalid 'source.sheet' in '{target_path}'.")

    metrics_list = data.get("metrics")
    if not isinstance(metrics_list, list):
        raise ValueError(f"INVALID_PREBUILT_REGISTRY_SCHEMA: 'metrics' in '{target_path}' must be a list.")

    if not metrics_list:
        raise ValueError("EMPTY_RISK_METRIC_SOURCE: Artifact metrics list is empty.")

    md_path = (target_path.parent / source_rel_path).resolve()
    if not md_path.exists():
        raise ValueError(
            f"STALE_PREBUILT_REGISTRY: Source Markdown file '{md_path}' referenced by '{target_path}' does not exist. "
            f"Run 'python -m app.mandate_risk.catalogue' to regenerate."
        )

    actual_sha256 = hashlib.sha256(md_path.read_bytes()).hexdigest()
    if actual_sha256 != expected_sha256:
        raise ValueError(
            f"STALE_PREBUILT_REGISTRY: Markdown source '{md_path}' hash ({actual_sha256}) "
            f"does not match artifact hash ({expected_sha256}). "
            f"Run 'python -m app.mandate_risk.catalogue' to update."
        )

    metrics: List[RawRiskMetric] = []
    seen_ids: Set[int] = set()
    seen_names: Set[str] = set()
    req_set = set(REQUIRED_FIELDS)

    for idx, item in enumerate(metrics_list):
        if not isinstance(item, dict):
            raise ValueError(f"INVALID_PREBUILT_REGISTRY_METRIC: Metric item #{idx} in '{target_path}' is not a JSON object.")

        if set(item.keys()) != req_set:
            raise ValueError(f"INVALID_PREBUILT_REGISTRY_METRIC: Metric item #{idx} in '{target_path}' does not match exact 10 required fields.")

        row_id = item["row_id"]
        if isinstance(row_id, bool) or not isinstance(row_id, int) or row_id <= 0:
            raise ValueError(f"INVALID_PREBUILT_REGISTRY_METRIC: 'row_id' in metric #{idx} must be positive integer, got {row_id!r}.")

        source_row = item["source_row"]
        if isinstance(source_row, bool) or not isinstance(source_row, int) or source_row <= 0:
            raise ValueError(f"INVALID_PREBUILT_REGISTRY_METRIC: 'source_row' in metric #{idx} must be positive integer, got {source_row!r}.")

        metric_name = item["metric_name"]
        if not isinstance(metric_name, str) or not metric_name.strip():
            raise ValueError(f"INVALID_PREBUILT_REGISTRY_METRIC: 'metric_name' in metric #{idx} must be non-blank string.")

        for str_key in ["raw_risk_type_1", "raw_risk_type_2", "effective_risk_type_1", "effective_risk_type_2", "algorithm", "mandate", "strategy_type"]:
            if not isinstance(item[str_key], str):
                raise ValueError(f"INVALID_PREBUILT_REGISTRY_METRIC: Field '{str_key}' in metric #{idx} must be string.")

        if row_id in seen_ids:
            raise ValueError(f"DUPLICATE_RISK_METRIC_ROW_ID: Duplicate row_id {row_id} in '{target_path}'")
        seen_ids.add(row_id)

        clean_name = metric_name.strip()
        if clean_name in seen_names:
            raise ValueError(f"DUPLICATE_RISK_METRIC_NAME: Duplicate metric_name {clean_name!r} in '{target_path}'")
        seen_names.add(clean_name)

        metric = RawRiskMetric(
            row_id=row_id,
            source_row=source_row,
            raw_risk_type_1=item["raw_risk_type_1"],
            raw_risk_type_2=item["raw_risk_type_2"],
            metric_name=clean_name,
            algorithm=item["algorithm"],
            mandate=item["mandate"],
            strategy_type=item["strategy_type"],
            effective_risk_type_1=item["effective_risk_type_1"],
            effective_risk_type_2=item["effective_risk_type_2"],
        )
        metrics.append(metric)

    return RawRiskMetricRegistry(
        metrics,
        source_path=str(target_path),
        source_sha256=expected_sha256,
        source_sheet=sheet_name,
    )


def main(argv: Optional[List[str]] = None) -> int:
    """CLI entrypoint for building or checking the risk metric catalogue JSON artifact."""
    parser = argparse.ArgumentParser(
        description="Compile or check canonical Markdown risk metric knowledge base artifact."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check that prebuilt JSON artifact is up to date without writing.",
    )
    parser.add_argument(
        "--source",
        type=str,
        default=None,
        help="Path to canonical Markdown source file (default: repo root 指标知识库.md).",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Path to output prebuilt JSON artifact file (default: repo root 指标知识库.generated.json).",
    )

    args = parser.parse_args(argv)

    source_path = (
        Path(args.source) if args.source else get_default_markdown_path()
    )
    output_path = (
        Path(args.output) if args.output else get_default_artifact_path()
    )

    try:
        payload = compile_catalogue(
            source_path=source_path,
            output_path=output_path,
            check_only=args.check,
        )
        metric_count = len(payload.get("metrics", []))
        sha256_hash = payload.get("source", {}).get("sha256", "")
        if args.check:
            print(
                f"SUCCESS: Artifact '{output_path}' is up-to-date with '{source_path}' "
                f"({metric_count} metrics, sha256: {sha256_hash[:12]}...)."
            )
        else:
            print(
                f"SUCCESS: Compiled '{source_path}' into '{output_path}' "
                f"({metric_count} metrics, sha256: {sha256_hash[:12]}...)."
            )
        return 0
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
