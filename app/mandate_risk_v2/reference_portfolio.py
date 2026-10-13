from __future__ import annotations

from datetime import datetime, timedelta, timezone
import json
import logging
import os
from pathlib import Path
from typing import Any, Literal, Sequence

from pydantic import Field

from app.mandate_risk_v2.models import StrictModel

logger = logging.getLogger("mandate_risk_v2.reference_portfolio")

DEFAULT_SNAPSHOT_NAME = "参考组合.snapshot.json"
DEFAULT_MAPPING_NAME = "参考组合映射.json"
SCHEMA_VERSION = 1


def get_repo_root() -> Path:
    """Return the backend repository root directory."""
    return Path(__file__).resolve().parents[2]


def get_default_snapshot_path() -> Path:
    """Return default snapshot JSON path at repo root or via env override."""
    env_path = os.getenv("MANDATE_RISK_REFERENCE_SNAPSHOT_PATH")
    if env_path and env_path.strip():
        return Path(env_path.strip()).expanduser().resolve()
    return (get_repo_root() / DEFAULT_SNAPSHOT_NAME).resolve()


def get_default_mapping_path() -> Path:
    """Return default mapping JSON path at repo root or via env override."""
    env_path = os.getenv("MANDATE_RISK_REFERENCE_MAPPING_PATH")
    if env_path and env_path.strip():
        return Path(env_path.strip()).expanduser().resolve()
    return (get_repo_root() / DEFAULT_MAPPING_NAME).resolve()


def current_china_date() -> str:
    """Return the current date in China (UTC+8) formatted as YYYY-MM-DD."""
    cst = timezone(timedelta(hours=8))
    return datetime.now(cst).strftime("%Y-%m-%d")


class ReferencePortfolioItem(StrictModel):
    """One matched reference portfolio configuration entry for an indicator."""

    port_code: str
    port_name: str
    config_id: str
    effective_date: str
    index_code: str
    index_name: str
    index_type: str | None = None
    green_rule: str | None = None
    green_value: float | int | str | None = None
    amber_rule: str | None = None
    amber_value: float | int | str | None = None
    red_rule: str | None = None
    red_value: float | int | str | None = None

class ReferencePortfolioSource(StrictModel):
    """Metadata describing the origin, currency, and availability of reference portfolios."""

    snapshot_exported_at: str | None = None
    as_of_date: str
    source_name: str
    status: Literal["ready", "unavailable"]


class ReferencePortfolioResolver:
    """Deterministic resolver reading validated local snapshot and explicit mapping.

    Version precedence & eligibility:
    1. Only configurations with non-empty effective_date <= as_of_date are eligible.
    2. If begin_date is present, must be <= as_of_date.
    3. If end_date is present, must be >= as_of_date (end_date inclusive).
    4. Select ONE current configuration per port using deterministic tie-breaking:
       latest effective_date, then updated_at, then ID.
    5. Details are matched strictly against the selected current config;
       historical configurations are never resurrected when current lacks the metric.
    6. Deduplication by port_code, stable deterministic sort by port_code.
    """

    def __init__(
        self,
        snapshot_path: str | Path | None = None,
        mapping_path: str | Path | None = None,
        as_of_date: str | None = None,
    ) -> None:
        self.snapshot_path = Path(snapshot_path).resolve() if snapshot_path else get_default_snapshot_path()
        self.mapping_path = Path(mapping_path).resolve() if mapping_path else get_default_mapping_path()
        self.as_of_date = as_of_date.strip() if as_of_date and as_of_date.strip() else current_china_date()

        self._snapshot_data: dict[str, Any] | None = None
        self._mappings: dict[str, str] = {}
        self._status: Literal["ready", "unavailable"] = "unavailable"
        self._exported_at: str | None = None
        self._source_name: str = "AMC_TYJX (ET_PORT_KCINDEX_CONFIG)"
        self._selected_configs_by_port: dict[str, dict[str, Any]] = {}
        self._details_by_config: dict[str, list[dict[str, Any]]] = {}

        self._load()

    def _load(self) -> None:
        # 1. Load mapping from maintainable JSON artifact
        if not self.mapping_path.exists():
            logger.info("Reference portfolio mapping not found at %s; status=unavailable", self.mapping_path)
            self._status = "unavailable"
            return

        try:
            map_content = json.loads(self.mapping_path.read_text(encoding="utf-8"))
        except Exception as exc:
            logger.warning("Invalid reference portfolio mapping JSON in %s: %s", self.mapping_path, exc)
            self._status = "unavailable"
            return

        if not isinstance(map_content, dict):
            logger.warning("Reference portfolio mapping root is not an object in %s", self.mapping_path)
            self._status = "unavailable"
            return

        raw_mappings = map_content.get("mappings")
        if not isinstance(raw_mappings, dict):
            logger.warning("Reference portfolio mapping 'mappings' is not an object in %s", self.mapping_path)
            self._status = "unavailable"
            return

        valid_mappings: dict[str, str] = {}
        for k, v in raw_mappings.items():
            if isinstance(k, str) and k.strip() and isinstance(v, str) and v.strip():
                valid_mappings[k.strip()] = v.strip()
            else:
                logger.warning("Invalid mapping entry in %s: %r -> %r", self.mapping_path, k, v)
        self._mappings = valid_mappings
        # 2. Load snapshot
        if not self.snapshot_path.exists():
            logger.info("Reference portfolio snapshot not found at %s; status=unavailable", self.snapshot_path)
            self._status = "unavailable"
            return

        try:
            raw_data = json.loads(self.snapshot_path.read_text(encoding="utf-8"))
        except Exception as exc:
            logger.warning("Invalid reference portfolio snapshot JSON in %s: %s", self.snapshot_path, exc)
            self._status = "unavailable"
            return

        if not isinstance(raw_data, dict) or raw_data.get("schema_version") != SCHEMA_VERSION:
            logger.warning("Reference portfolio snapshot schema_version invalid or missing in %s", self.snapshot_path)
            self._status = "unavailable"
            return

        configs = raw_data.get("configs")
        details = raw_data.get("details")
        if not isinstance(configs, list) or not isinstance(details, list):
            logger.warning("Reference portfolio snapshot missing configs or details array in %s", self.snapshot_path)
            self._status = "unavailable"
            return

        self._snapshot_data = raw_data
        self._exported_at = raw_data.get("exported_at")
        src_meta = raw_data.get("source")
        if isinstance(src_meta, dict) and src_meta.get("connection_name"):
            self._source_name = str(src_meta["connection_name"])

        # 3. Filter started configs by date policy (missing date cannot silently current)
        started_by_port: dict[str, list[dict[str, Any]]] = {}
        for c in configs:
            if not isinstance(c, dict):
                continue
            eff = c.get("effective_date")
            # Never infer missing start dates
            if not eff or not str(eff).strip():
                continue
            eff_str = str(eff).strip()
            if eff_str > self.as_of_date:
                continue

            beg = c.get("begin_date")
            if beg and str(beg).strip() > self.as_of_date:
                continue

            port = str(c.get("port_code") or "").strip()
            if not port:
                continue
            started_by_port.setdefault(port, []).append(c)

        # 4. Deterministic latest started config selection per port: effective_date -> updated_at -> ID
        # Once a newer already-started config supersedes an older one, older END_DATE=null cannot
        # reappear even if newer later expires; check expiry on the latest started config with no historical fallback.
        self._selected_configs_by_port = {}
        for port, port_configs in started_by_port.items():
            latest_config = max(
                port_configs,
                key=lambda item: (
                    str(item.get("effective_date") or "").strip(),
                    str(item.get("updated_at") or "").strip(),
                    str(item.get("id") or "").strip(),
                ),
            )
            end = latest_config.get("end_date")
            if end and str(end).strip() and str(end).strip() < self.as_of_date:
                # Latest started config has expired; no historical fallback
                continue
            self._selected_configs_by_port[port] = latest_config
        # 5. Index details by config_id
        self._details_by_config = {}
        for d in details:
            if isinstance(d, dict) and d.get("config_id"):
                cfg_id = str(d["config_id"])
                self._details_by_config.setdefault(cfg_id, []).append(d)

        self._status = "ready"

    def is_ready(self) -> bool:
        """Return True if the snapshot was loaded and is ready for querying."""
        return self._status == "ready"

    def get_source(self) -> ReferencePortfolioSource:
        """Return structured reference portfolio provenance metadata."""
        return ReferencePortfolioSource(
            snapshot_exported_at=self._exported_at,
            as_of_date=self.as_of_date,
            source_name=self._source_name,
            status=self._status,
        )

    def get_index_code(self, metric_name: str) -> str | None:
        """Return mapped INDEX_CODE for canonical or alias metric name, or None if unmapped."""
        if not metric_name:
            return None
        return self._mappings.get(metric_name.strip())

    def resolve(self, metric_name: str) -> list[ReferencePortfolioItem]:
        """Resolve applicable reference portfolios for a metric name."""
        if not self.is_ready():
            return []

        index_code = self.get_index_code(metric_name)
        if not index_code:
            return []

        results: list[ReferencePortfolioItem] = []
        seen_ports: set[str] = set()

        for port in sorted(self._selected_configs_by_port.keys()):
            if port in seen_ports:
                continue
            cfg = self._selected_configs_by_port[port]
            cfg_id = str(cfg.get("id") or "")
            cfg_details = self._details_by_config.get(cfg_id, [])

            match_detail = next((d for d in cfg_details if d.get("index_code") == index_code), None)
            if match_detail is not None:
                seen_ports.add(port)
                results.append(
                    ReferencePortfolioItem(
                        port_code=str(cfg.get("port_code") or port),
                        port_name=str(cfg.get("port_name")) if cfg.get("port_name") is not None else "",
                        config_id=cfg_id,
                        effective_date=str(cfg.get("effective_date") or ""),
                        index_code=str(match_detail.get("index_code") or index_code),
                        index_name=str(match_detail.get("index_name") or ""),
                        index_type=str(match_detail.get("index_type")) if match_detail.get("index_type") is not None else None,
                        green_rule=str(match_detail.get("green_rule")) if match_detail.get("green_rule") is not None else None,
                        green_value=match_detail.get("green_value"),
                        amber_rule=str(match_detail.get("amber_rule")) if match_detail.get("amber_rule") is not None else None,
                        amber_value=match_detail.get("amber_value"),
                        red_rule=str(match_detail.get("red_rule")) if match_detail.get("red_rule") is not None else None,
                        red_value=match_detail.get("red_value"),
                    )
                )

        return results

    @staticmethod
    def format_reference_cell(portfolios: Sequence[ReferencePortfolioItem]) -> str:
        """Format reference portfolios for fallback markdown table column."""
        if not portfolios:
            return "—"
        names = [p.port_name or p.port_code for p in portfolios if (p.port_name or p.port_code)]
        return "、".join(names) if names else "—"

    def enrich_metrics(self, metrics: Sequence[Any]) -> list[Any]:
        """Enrich a sequence of MatchedMetricResult with reference portfolios."""
        for item in metrics:
            metric_name = getattr(getattr(item, "metric", None), "metric_name", "")
            item.reference_portfolios = self.resolve(metric_name)
        return list(metrics)

    def enrich_result(self, result: Any) -> Any:
        """Enrich a V2AnalysisResult instance with reference portfolios and source metadata."""
        if result is None:
            return None

        result.reference_portfolio_source = self.get_source()
        self.enrich_metrics(getattr(result, "screened_metrics", []))
        self.enrich_metrics(getattr(result, "matched_metrics", []))
        self.enrich_metrics(getattr(result, "candidate_metrics", []))
        return result
