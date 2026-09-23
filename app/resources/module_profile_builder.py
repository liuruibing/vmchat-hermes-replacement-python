import json
import re
from typing import Any, Dict, Iterable, List, Optional


MERGE_GUIDANCE_V2 = """
# 跨模块合并语义指引 v2

这是运行时生成的结构化语义规则。发生冲突时，本文件优先于旧版 merge-rules.md。

## 证据优先级

1. catalog/profiles/<moduleId>.json 中的 shape、entity、grain、joinKeys、taxonomy、sqlEvidence。
2. 模块样例 JSON 中稳定出现的结构字段，只用于判断粒度、公共键、分类体系和数据形态。
3. 模块字段映射，用于决定最终可展示字段、单位和格式。
4. Wiki 自然语言说明仅作补充；描述笼统不能推翻结构化证据。

profile 中 structuralOnlyFields 允许在 transform 中作为关联键使用，但不能作为最终 table 列或 ECharts series 展示。

## 默认合并意图

用户说“放在一起”“一起看”“同表展示”“对比”“合并展示”，且没有明确要求纵向拼接时，
默认按公共业务键做横向关联，不需要再次询问横向还是纵向。

## 横向合并

满足以下条件时优先允许：

- entity 一致；
- 至少有一个相同 canonical join key，例如 date、industry、security、asset_class；
- 相同 canonical key 的原始字段名可以不同，例如 TDATE、D_DATE、XAXISDATA 都可标准化为 date；
- 分类数据如果声明 taxonomy，则 taxonomy 必须一致；
- 不需要临时聚合、重采样或多对多展开。

数据集合不完全重合不是拒绝理由，使用 outer join 思路：键取合集，缺失侧填 null。

## 单位和视图

单位不同不是“不能合并数据”的理由。

- table：不同指标保留独立列、单位和格式。
- ECharts：最多两个 Y 轴。
- 用户未强制图表时，超过两个不兼容量纲应优先选择 table，而不是拒绝合并。
- 用户明确要求 ECharts 且超过两个不兼容量纲时，再请求缩减指标或拆图。

## 典型模式

- 产品时序：entity=fund、shape=time_series、joinKeys 包含 date，可按日期横向关联。
- 行业截面：entity=fund、shape=cross_section、joinKeys 包含 industry，且 taxonomy 一致，可按 industryCode 优先、industryName 兜底关联。
- 单行指标：多个 scalar_or_single_row 且 entity 一致，可合并为单行宽表。

## 必须拒绝

- entity 明确冲突；
- 没有可信公共 canonical key，且不是同实体单行指标；
- taxonomy 明确冲突；
- 只能按数组下标对齐；
- 必须先聚合、去重、重采样或解决多对多关系；
- 业务字段含义无法唯一确定。

## DSL 生成

先在内部形成 merge plan，再生成 DSL。每个 request 保留独立 moduleId/sqlCode；
transform 按 canonical key 显式对齐；join key 可以来自 structuralOnlyFields；
最终 view 只能暴露字段映射允许展示的字段。
""".strip()


def _unique(values: Iterable[str]) -> List[str]:
    result: List[str] = []
    seen = set()
    for value in values:
        text = str(value).strip()
        if text and text not in seen:
            seen.add(text)
            result.append(text)
    return result


def _front_matter(markdown: str) -> Dict[str, str]:
    match = re.match(r"---\s*\n(.*?)\n---\s*\n", markdown, re.S)
    if not match:
        return {}
    out: Dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        out[key.strip()] = value.strip().strip(chr(34)).strip(chr(39))
    return out


def _section(markdown: str, heading: str) -> str:
    match = re.search(r"^##\s+" + re.escape(heading) + r"\s*$", markdown, re.M)
    if not match:
        return ""
    start = match.end()
    next_heading = re.search(r"^##\s+", markdown[start:], re.M)
    end = start + next_heading.start() if next_heading else len(markdown)
    return markdown[start:end].strip()


def _raw_field(path: str) -> str:
    cleaned = path.replace("[]", "")
    return cleaned.split(".")[-1]


def _sample_json(markdown: str) -> Optional[Any]:
    body = _section(markdown, "示例 JSON 数据")
    fence = re.escape(chr(96) * 3)
    match = re.search(fence + r"json\s*(.*?)\s*" + fence, body, re.S | re.I)
    if not match:
        return None
    try:
        return json.loads(match.group(1))
    except Exception:
        return None


def _largest_rows(value: Any) -> List[Dict[str, Any]]:
    best: List[Dict[str, Any]] = []

    def visit(node: Any) -> None:
        nonlocal best
        if isinstance(node, list):
            if node and all(isinstance(item, dict) for item in node) and len(node) > len(best):
                best = list(node)
            for item in node:
                visit(item)
        elif isinstance(node, dict):
            for child in node.values():
                visit(child)

    visit(value)
    return best


def _looks_date(value: Any) -> bool:
    text = str(value or "").strip()
    return bool(
        re.fullmatch(r"\d{8}", text)
        or re.fullmatch(r"\d{4}-\d{2}-\d{2}(?:[ T].*)?", text)
        or re.fullmatch(r"\d{4}/\d{2}/\d{2}(?:[ T].*)?", text)
    )


def _candidates(render: str, label: str) -> List[Dict[str, str]]:
    lines = render.splitlines()
    active = False
    out: List[Dict[str, str]] = []
    marker = "- " + label + "："
    for line in lines:
        stripped = line.strip()
        if stripped == marker:
            active = True
            continue
        if active and stripped.startswith("- ") and not line.startswith(("  ", "\t")):
            break
        if not active:
            continue
        tick = chr(96)
        pattern = r"^\s*-\s*(.+?)（" + re.escape(tick) + r"([^" + re.escape(tick) + r"]+)" + re.escape(tick) + r"）\s*$"
        match = re.match(pattern, line)
        if match:
            out.append(
                {
                    "name": match.group(1).strip(),
                    "path": match.group(2).strip(),
                    "rawField": _raw_field(match.group(2).strip()),
                }
            )
    return out


def _field_mapping(markdown: str) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for line in _section(markdown, "字段映射").splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 6 or cells[0] == "JSON 路径" or set(cells[0]) <= set("-: "):
            continue
        out.append(
            {
                "jsonPath": cells[0].strip(chr(96)),
                "rawField": cells[1].strip(chr(96)),
                "displayName": cells[2],
                "transform": cells[3],
                "unit": cells[4],
                "views": [x.strip() for x in re.split(r"[、,，/]", cells[5]) if x.strip()],
            }
        )
    return out


def _canonical(name: str, raw: str, sample_value: Any = None) -> str:
    lower = raw.lower()
    if (
        any(token in name for token in ("日期", "时间", "估值日", "交易日"))
        or lower in {"tdate", "d_date", "trade_date", "date"}
        or (lower == "xaxisdata" and _looks_date(sample_value))
    ):
        return "date"
    if "行业" in name or "industry" in lower:
        return "industry"
    if any(token in name for token in ("证券", "股票", "债券", "个券", "合约", "品种")):
        return "security"
    if any(token in name for token in ("资产类别", "资产类型", "大类资产")):
        return "asset_class"
    return "category"


def _sql_sections(sql_document: str) -> Dict[str, str]:
    if not sql_document:
        return {}
    pattern = re.compile(
        r"^##\s+<a\s+id=[\"']module-([A-Za-z0-9]+)[\"']></a>.*$",
        re.M,
    )
    matches = list(pattern.finditer(sql_document))
    out: Dict[str, str] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(sql_document)
        out[match.group(1)] = sql_document[match.start():end]
    return out


def _sql_evidence(section: str) -> Dict[str, Any]:
    fence = re.escape(chr(96) * 3)
    match = re.search(fence + r"sql\s*(.*?)\s*" + fence, section or "", re.S | re.I)
    sql = match.group(1) if match else ""
    if not sql:
        return {"available": False}
    tables = _unique(
        m.group(1).upper()
        for m in re.finditer(r"\b(?:from|join)\s+([A-Za-z_][A-Za-z0-9_.$]*)", sql, re.I)
        if m.group(1).lower() != "dual"
    )
    normalized = re.sub(r"\s+", " ", sql)
    group_by_fields: List[str] = []
    for group_match in re.finditer(
        r"\bgroup\s+by\s+(.{1,500}?)(?=\border\s+by\b|\bhaving\b|\bunion\b|$)",
        normalized,
        re.I,
    ):
        group_by_fields.extend(
            re.findall(
                r"(?:[A-Za-z_][A-Za-z0-9_]*\.)?([A-Za-z_][A-Za-z0-9_]*)",
                group_match.group(1),
            )
        )
    return {
        "available": True,
        "tables": tables[:30],
        "params": _unique(re.findall(r"#\{([A-Za-z0-9_]+)\}", sql)),
        "groupByFields": _unique(group_by_fields)[:30],
        "flags": {
            "mentionsFund": bool(re.search(r"fundcode|#\{fundCode\}", sql, re.I)),
            "mentionsDate": bool(re.search(r"d_date|tdate|#\{beginDate\}|#\{endDate\}", sql, re.I)),
            "mentionsIndustry": bool(re.search(r"industry|indu|hy_", sql, re.I)),
            "hasUnion": bool(re.search(r"\bunion(?:\s+all)?\b", sql, re.I)),
            "hasWindowFunction": bool(re.search(r"\bover\s*\(", sql, re.I)),
        },
    }


def build_module_profile(module_id: str, markdown: str, sql_section: str = "") -> Dict[str, Any]:
    front = _front_matter(markdown)
    render = _section(markdown, "渲染能力")
    dimensions = _candidates(render, "维度候选")
    metrics = _candidates(render, "指标候选")
    fields = _field_mapping(markdown)
    sample = _sample_json(markdown)
    rows = _largest_rows(sample)
    row_keys = _unique(key for row in rows[:10] for key in row.keys())
    row_key_set = set(row_keys)

    join_keys: Dict[str, Dict[str, Any]] = {}

    def add_key(canonical: str, raw: str, evidence: str, primary: bool = False) -> None:
        item = join_keys.setdefault(
            canonical,
            {"canonical": canonical, "rawFields": [], "evidence": [], "primary": False},
        )
        if raw and raw not in item["rawFields"]:
            item["rawFields"].append(raw)
        if evidence not in item["evidence"]:
            item["evidence"].append(evidence)
        item["primary"] = item["primary"] or primary

    dimension_types: List[str] = []
    for dim in dimensions:
        values = [row.get(dim["rawField"]) for row in rows[:10] if dim["rawField"] in row]
        canonical = _canonical(dim["name"], dim["rawField"], values[0] if values else None)
        dim["canonical"] = canonical
        dimension_types.append(canonical)
        add_key(canonical, dim["rawField"], "render_dimension", True)

    for raw in ("FCODE", "VC_FUNDCODE"):
        if raw in row_key_set:
            add_key("fund", raw, "sample_json")

    for raw in ("TDATE", "D_DATE", "TRADE_DATE", "DATE", "XAXISDATA"):
        values = [row.get(raw) for row in rows[:10] if raw in row]
        if values and sum(1 for value in values if _looks_date(value)) >= max(1, len(values) // 2):
            add_key("date", raw, "sample_json", "date" in dimension_types)

    for raw in ("industryCode", "industryName"):
        if raw in row_key_set:
            add_key("industry", raw, "sample_json", "industry" in dimension_types)

    head = sample.get("head", {}) if isinstance(sample, dict) and isinstance(sample.get("head"), dict) else {}
    taxonomy = head.get("industryType")
    if not taxonomy and module_id.startswith("swIndu"):
        taxonomy = "SWSR"
    if not taxonomy and module_id.startswith("hsIndu"):
        taxonomy = "HS_CUSTOM"

    entity = "fund" if "fund" in join_keys or front.get("templateType") == "single-product-performance" else "unknown"
    if "date" in dimension_types:
        shape = "time_series"
    elif dimensions:
        shape = "cross_section"
    elif len(rows) <= 1:
        shape = "scalar_or_single_row"
    else:
        shape = "tabular"

    renderable = {field["rawField"] for field in fields}
    structural_only = _unique(
        raw
        for item in join_keys.values()
        for raw in item["rawFields"]
        if raw not in renderable
    )

    default_match = re.search(r"-\s*默认视图：\s*([^\n]+)", render)
    return {
        "schemaVersion": "2.0",
        "moduleId": module_id,
        "title": front.get("title") or module_id,
        "sqlCode": front.get("sqlId"),
        "shape": shape,
        "entity": entity,
        "grain": {
            "primaryCanonicalKeys": _unique(dimension_types) or (["fund"] if shape == "scalar_or_single_row" and entity == "fund" else []),
            "contextCanonicalKeys": [key for key in ("fund", "date") if key in join_keys],
        },
        "joinKeys": list(join_keys.values()),
        "taxonomy": taxonomy,
        "render": {
            "defaultView": default_match.group(1).strip() if default_match else None,
            "dimensions": dimensions,
            "metrics": metrics,
        },
        "fields": fields,
        "structuralOnlyFields": structural_only,
        "sample": {"rowCount": len(rows), "rowKeys": row_keys, "head": head},
        "sqlEvidence": _sql_evidence(sql_section),
    }


def build_module_profiles(module_markdown_map: Dict[str, str], sql_document: str = "") -> Dict[str, Dict[str, Any]]:
    sections = _sql_sections(sql_document)
    return {
        module_id: build_module_profile(module_id, markdown, sections.get(module_id, ""))
        for module_id, markdown in module_markdown_map.items()
    }


def build_profile_index(profiles: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    modules: Dict[str, Any] = {}
    for module_id, profile in profiles.items():
        modules[module_id] = {
            "title": profile.get("title"),
            "shape": profile.get("shape"),
            "entity": profile.get("entity"),
            "grain": profile.get("grain"),
            "joinKeys": [
                {
                    "canonical": item.get("canonical"),
                    "rawFields": item.get("rawFields"),
                    "primary": item.get("primary"),
                }
                for item in profile.get("joinKeys", [])
            ],
            "taxonomy": profile.get("taxonomy"),
            "defaultView": (profile.get("render") or {}).get("defaultView"),
            "sqlEvidenceAvailable": bool((profile.get("sqlEvidence") or {}).get("available")),
        }
    return {
        "schemaVersion": "2.0",
        "description": "由模块字段映射、样例 JSON 和可选 SQL 文档自动提取的运行时结构化语义索引。",
        "modules": modules,
    }
