from __future__ import annotations

import re
from typing import Any, Dict, List, Sequence


def _norm(text: Any) -> str:
    return re.sub(r"[^a-z0-9\u3400-\u9fff]+", "", str(text or "").lower())


def _metric_unit(profile: Dict[str, Any], raw_field: str) -> str | None:
    for field in profile.get("fields") or []:
        if not isinstance(field, dict):
            continue
        if str(field.get("rawField") or "") == raw_field:
            unit = str(field.get("unit") or "").strip()
            return unit or None
    return None


def resolve_metrics(user_message: str, resources: Any) -> List[Dict[str, Any]]:
    """Resolve explicitly mentioned display metrics from the runtime profile index.

    This deliberately favors high precision over recall. The LLM can still use
    knowledge retrieval for ambiguous phrasing; deterministic matches become
    strong hints rather than replacing model understanding.
    """

    query = _norm(user_message)
    if not query:
        return []

    profiles = getattr(resources, "moduleProfiles", None) or getattr(
        resources, "module_profiles", None
    ) or {}
    matches: List[Dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()

    for module_id, profile in profiles.items():
        render = (profile or {}).get("render") or {}
        for metric in render.get("metrics") or []:
            if not isinstance(metric, dict):
                continue
            name = str(metric.get("name") or "").strip()
            raw_field = str(metric.get("rawField") or "").strip()
            normalized = _norm(name)
            if not normalized or normalized not in query:
                continue
            key = (str(module_id), raw_field or normalized)
            if key in seen:
                continue
            seen.add(key)
            matches.append(
                {
                    "name": name,
                    "moduleId": str(module_id),
                    "rawField": raw_field or None,
                    "unit": _metric_unit(profile, raw_field),
                    "entity": profile.get("entity"),
                    "shape": profile.get("shape"),
                    "grain": (profile.get("grain") or {}).get("primaryCanonicalKeys") or [],
                    "taxonomy": profile.get("taxonomy"),
                }
            )

    # Longer names first keeps "股票净敞口占比" ahead of a shorter overlapping
    # metric if both exist in the catalog.
    matches.sort(key=lambda item: len(_norm(item.get("name"))), reverse=True)
    return matches[:20]


def build_semantic_plan(
    resolved_metrics: Sequence[Dict[str, Any]],
    resources: Any,
) -> Dict[str, Any]:
    module_ids: List[str] = []
    for item in resolved_metrics:
        module_id = str(item.get("moduleId") or "")
        if module_id and module_id not in module_ids:
            module_ids.append(module_id)

    if not module_ids:
        return {
            "status": "unresolved",
            "mergeable": None,
            "reason": "no_deterministic_metric_match",
            "moduleIds": [],
        }

    profiles = getattr(resources, "moduleProfiles", None) or getattr(
        resources, "module_profiles", None
    ) or {}
    selected = [profiles[mid] for mid in module_ids if mid in profiles]
    if not selected:
        return {
            "status": "unresolved",
            "mergeable": None,
            "reason": "profiles_missing",
            "moduleIds": module_ids,
        }

    entities = {str(p.get("entity") or "unknown") for p in selected}
    shapes = {str(p.get("shape") or "unknown") for p in selected}
    taxonomies = {
        str(p.get("taxonomy"))
        for p in selected
        if p.get("taxonomy") not in (None, "")
    }
    grain_sets = [
        set((p.get("grain") or {}).get("primaryCanonicalKeys") or [])
        for p in selected
    ]

    plan: Dict[str, Any] = {
        "status": "planned",
        "mergeable": True,
        "moduleIds": module_ids,
        "entities": sorted(entities),
        "shapes": sorted(shapes),
        "taxonomies": sorted(taxonomies),
        "joinKey": None,
        "reason": "compatible",
    }

    if len(module_ids) == 1:
        keys = list(grain_sets[0]) if grain_sets else []
        plan["joinKey"] = keys[0] if keys else None
        plan["reason"] = "single_module"
        return plan

    if "unknown" in entities or len(entities) != 1:
        plan.update(
            mergeable=False,
            reason="entity_unknown_or_mismatch",
        )
        return plan

    if len(shapes) != 1:
        # Multiple single-row sources are the one safe shape exception.
        if shapes != {"scalar_or_single_row"}:
            plan.update(
                mergeable=False,
                reason="shape_mismatch",
            )
            return plan

    if len(taxonomies) > 1:
        plan.update(
            mergeable=False,
            reason="taxonomy_mismatch",
        )
        return plan

    if shapes == {"scalar_or_single_row"}:
        plan["reason"] = "same_entity_scalar"
        return plan

    common = set.intersection(*grain_sets) if grain_sets else set()
    preferred = ["date", "industry", "security", "asset_class", "fund"]
    join_key = next((key for key in preferred if key in common), None)
    if join_key is None and common:
        join_key = sorted(common)[0]

    if join_key is None:
        plan.update(
            mergeable=False,
            reason="no_common_primary_grain",
        )
        return plan

    plan["joinKey"] = join_key
    plan["reason"] = "common_primary_grain"
    return plan
