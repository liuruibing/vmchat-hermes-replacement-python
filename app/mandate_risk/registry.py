from __future__ import annotations

import csv
import hashlib
import re
import zipfile
from pathlib import Path, PurePosixPath
from typing import Dict, Iterable, List, Optional
from xml.etree import ElementTree as ET

from app.mandate_risk.models import RawRiskMetric


EXPECTED_HEADERS = [
    "风险类型一级",
    "风险类型二级",
    "指标名称",
    "指标算法",
    "Mandate字段",
    "适用策略种类",
]

_MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
_REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
_PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"


def _text(value: object) -> str:
    return "" if value is None else str(value)


def _strategy_tokens(raw: str) -> set[str]:
    normalized = (raw or "").replace("／", "/")
    return {item.strip() for item in normalized.split("/") if item.strip()}


# The snapshot marks turnover as equity-only, although its Mandate field also
# names the fixed-income Buy and Maintain strategy. Keep the source row intact.
_DERIVED_STRATEGY_TYPES = {"换手率(%)": {"固收"}}


def _col_index(cell_ref: str) -> int:
    match = re.match(r"([A-Z]+)", cell_ref or "")
    if not match:
        return -1
    value = 0
    for char in match.group(1):
        value = value * 26 + (ord(char) - ord("A") + 1)
    return value - 1


def _xlsx_sheet_target(archive: zipfile.ZipFile, sheet_name: str) -> str:
    workbook = ET.fromstring(archive.read("xl/workbook.xml"))
    rels = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
    rel_map = {
        rel.attrib.get("Id", ""): rel.attrib.get("Target", "")
        for rel in rels.findall(f"{{{_PKG_REL_NS}}}Relationship")
    }
    for sheet in workbook.findall(f".//{{{_MAIN_NS}}}sheet"):
        if sheet.attrib.get("name") != sheet_name:
            continue
        rel_id = sheet.attrib.get(f"{{{_REL_NS}}}id", "")
        target = rel_map.get(rel_id)
        if not target:
            break
        if target.startswith("/"):
            return target.lstrip("/")
        return str(PurePosixPath("xl") / target)
    raise ValueError(f"RISK_METRIC_SHEET_NOT_FOUND: {sheet_name}")


def _shared_strings(archive: zipfile.ZipFile) -> List[str]:
    if "xl/sharedStrings.xml" not in archive.namelist():
        return []
    root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
    result: List[str] = []
    for item in root.findall(f"{{{_MAIN_NS}}}si"):
        parts = [node.text or "" for node in item.findall(f".//{{{_MAIN_NS}}}t")]
        result.append("".join(parts))
    return result


def _cell_value(cell: ET.Element, shared: List[str]) -> str:
    cell_type = cell.attrib.get("t", "")
    if cell_type == "inlineStr":
        parts = [node.text or "" for node in cell.findall(f".//{{{_MAIN_NS}}}t")]
        return "".join(parts)
    value_node = cell.find(f"{{{_MAIN_NS}}}v")
    if value_node is None or value_node.text is None:
        return ""
    raw = value_node.text
    if cell_type == "s":
        try:
            return shared[int(raw)]
        except Exception:
            return raw
    return raw


def _read_sheet_values(path: Path, sheet_name: str) -> List[List[str]]:
    with zipfile.ZipFile(path, "r") as archive:
        target = _xlsx_sheet_target(archive, sheet_name)
        shared = _shared_strings(archive)
        root = ET.fromstring(archive.read(target))
        rows: Dict[int, List[str]] = {}
        max_row = 0
        for row_node in root.findall(f".//{{{_MAIN_NS}}}row"):
            row_number = int(row_node.attrib.get("r") or 0)
            if row_number <= 0:
                continue
            max_row = max(max_row, row_number)
            values = [""] * 6
            for cell in row_node.findall(f"{{{_MAIN_NS}}}c"):
                idx = _col_index(cell.attrib.get("r", ""))
                if 0 <= idx < 6:
                    values[idx] = _cell_value(cell, shared)
            rows[row_number] = values
        return [rows.get(index, [""] * 6) for index in range(1, max_row + 1)]


def _read_csv_values(path: Path) -> List[List[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [[_text(cell) for cell in row] for row in csv.reader(handle)]


def _build_rows(values: List[List[str]]) -> List[RawRiskMetric]:
    if not values:
        raise ValueError("EMPTY_RISK_METRIC_SOURCE")
    headers = values[0]
    if headers != EXPECTED_HEADERS:
        raise ValueError("INVALID_RISK_METRIC_HEADERS: " + ",".join(headers))

    result: List[RawRiskMetric] = []
    last_type_1 = ""
    last_type_2 = ""
    for source_row, raw_values in enumerate(values[1:], start=2):
        padded = list(raw_values[:6]) + [""] * max(0, 6 - len(raw_values))
        raw_type_1, raw_type_2, metric_name, algorithm, mandate, strategy_type = [
            _text(value) for value in padded[:6]
        ]
        if raw_type_1:
            last_type_1 = raw_type_1
        if raw_type_2:
            last_type_2 = raw_type_2
        if not metric_name:
            continue
        result.append(
            RawRiskMetric(
                row_id=source_row,
                source_row=source_row,
                raw_risk_type_1=raw_type_1,
                raw_risk_type_2=raw_type_2,
                metric_name=metric_name,
                algorithm=algorithm,
                mandate=mandate,
                strategy_type=strategy_type,
                effective_risk_type_1=last_type_1,
                effective_risk_type_2=last_type_2,
            )
        )
    return result


class RawRiskMetricRegistry:
    """Read-only registry backed by an immutable snapshot of the authoritative sheet.

    The source workbook remains the business source of truth. The repository ships an
    exact UTF-8 CSV snapshot of ``AI测试样例信息.xlsx#风险指标库`` so CI/deployments can
    read source cell values without rewriting, correcting or forward-filling them.
    Derived effective group labels live in separate fields only.
    """

    def __init__(
        self,
        rows: Iterable[RawRiskMetric],
        *,
        source_path: str = "",
        source_sha256: str = "",
        source_sheet: str = "风险指标库",
    ) -> None:
        self.source_path = source_path
        self.source_sha256 = source_sha256
        self.source_sheet = source_sheet
        self._rows = list(rows)
        self._by_id: Dict[int, RawRiskMetric] = {item.row_id: item for item in self._rows}
        self._by_name: Dict[str, RawRiskMetric] = {item.metric_name: item for item in self._rows}
        if len(self._by_id) != len(self._rows):
            raise ValueError("DUPLICATE_RISK_METRIC_ROW_ID")
        if len(self._by_name) != len(self._rows):
            raise ValueError("DUPLICATE_RISK_METRIC_NAME")

    @classmethod
    def from_xlsx(
        cls,
        path: str | Path,
        sheet_name: str = "风险指标库",
    ) -> "RawRiskMetricRegistry":
        source = Path(path)
        source_bytes = source.read_bytes()
        return cls(
            _build_rows(_read_sheet_values(source, sheet_name)),
            source_path=str(source),
            source_sha256=hashlib.sha256(source_bytes).hexdigest(),
            source_sheet=sheet_name,
        )

    @classmethod
    def from_csv(
        cls,
        path: str | Path,
        sheet_name: str = "风险指标库",
    ) -> "RawRiskMetricRegistry":
        source = Path(path)
        source_bytes = source.read_bytes()
        return cls(
            _build_rows(_read_csv_values(source)),
            source_path=str(source),
            source_sha256=hashlib.sha256(source_bytes).hexdigest(),
            source_sheet=sheet_name,
        )

    @classmethod
    def from_path(
        cls,
        path: str | Path,
        sheet_name: str = "风险指标库",
    ) -> "RawRiskMetricRegistry":
        source = Path(path)
        if source.suffix.lower() == ".xlsx":
            return cls.from_xlsx(source, sheet_name)
        if source.suffix.lower() == ".csv":
            return cls.from_csv(source, sheet_name)
        raise ValueError(f"UNSUPPORTED_RISK_METRIC_SOURCE: {source.suffix}")

    def all(self) -> List[RawRiskMetric]:
        return list(self._rows)

    def get(self, row_id: int) -> Optional[RawRiskMetric]:
        return self._by_id.get(int(row_id))

    def require(self, row_id: int) -> RawRiskMetric:
        metric = self.get(row_id)
        if metric is None:
            raise ValueError(f"UNKNOWN_RISK_METRIC_ROW: {row_id}")
        return metric

    def get_by_name(self, name: str) -> Optional[RawRiskMetric]:
        return self._by_name.get(str(name or ""))

    def eligible_for_strategy(self, strategy_type: str) -> List[RawRiskMetric]:
        strategy = str(strategy_type or "").strip()
        if not strategy or strategy == "未知" or strategy == "混合":
            return self.all()

        result: List[RawRiskMetric] = []
        for row in self._rows:
            tokens = _strategy_tokens(row.strategy_type)
            if (
                not tokens
                or strategy in tokens
                or "基金层" in tokens
                or strategy in _DERIVED_STRATEGY_TYPES.get(row.metric_name, set())
            ):
                result.append(row)
        return result
