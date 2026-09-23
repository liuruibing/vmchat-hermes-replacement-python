import argparse
import json
import os
from typing import Any, Dict, List

from app.resources import ResourceLoader


def _load_profile(resources: Any, module_id: str) -> Dict[str, Any]:
    path = f"catalog/profiles/{module_id}.json"
    raw = resources.toolResourceTextByPath.get(path)
    if raw is None:
        raise SystemExit(f"Unknown moduleId: {module_id}")
    return json.loads(raw)


def _canonical_keys(profile: Dict[str, Any]) -> set[str]:
    return {
        str(item.get("canonical"))
        for item in profile.get("joinKeys", [])
        if item.get("canonical")
    }


def _assess(profiles: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not profiles:
        return {"status": "unknown", "reason": "no profiles"}

    entities = {profile.get("entity") for profile in profiles}
    if len(entities) > 1:
        return {
            "status": "incompatible",
            "reason": "entity mismatch",
            "entities": sorted(str(x) for x in entities),
        }

    taxonomies = {
        profile.get("taxonomy")
        for profile in profiles
        if profile.get("taxonomy")
    }
    key_sets = [_canonical_keys(profile) for profile in profiles]
    common_keys = set.intersection(*key_sets) if key_sets else set()

    if "industry" in common_keys and len(taxonomies) > 1:
        return {
            "status": "incompatible",
            "reason": "taxonomy mismatch",
            "taxonomies": sorted(str(x) for x in taxonomies),
        }

    if common_keys:
        return {
            "status": "compatible",
            "strategy": "horizontal",
            "commonCanonicalKeys": sorted(common_keys),
        }

    if all(profile.get("shape") == "scalar_or_single_row" for profile in profiles):
        return {
            "status": "compatible",
            "strategy": "single_row",
            "commonCanonicalKeys": ["fund"],
        }

    return {
        "status": "unknown",
        "reason": "no common canonical join key",
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Inspect generated semantic profiles and merge compatibility."
    )
    parser.add_argument("module_ids", nargs="+", help="One or more VM moduleIds")
    parser.add_argument(
        "--resources-dir",
        default=os.getenv("VMCHAT_RESOURCES_DIR", "resources"),
        help="Resources directory. Defaults to VMCHAT_RESOURCES_DIR or ./resources.",
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Print full generated profiles instead of compact summaries.",
    )
    args = parser.parse_args()

    resources = ResourceLoader(args.resources_dir).load_sync()
    profiles = [_load_profile(resources, module_id) for module_id in args.module_ids]

    if args.full:
        print(json.dumps(profiles, ensure_ascii=False, indent=2))
    else:
        summaries = []
        for profile in profiles:
            summaries.append(
                {
                    "moduleId": profile.get("moduleId"),
                    "title": profile.get("title"),
                    "shape": profile.get("shape"),
                    "entity": profile.get("entity"),
                    "taxonomy": profile.get("taxonomy"),
                    "joinKeys": profile.get("joinKeys"),
                    "quality": profile.get("quality"),
                    "sqlEvidence": profile.get("sqlEvidence"),
                }
            )
        print(json.dumps(summaries, ensure_ascii=False, indent=2))

    if len(profiles) > 1:
        print("\nMERGE ASSESSMENT")
        print(json.dumps(_assess(profiles), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
