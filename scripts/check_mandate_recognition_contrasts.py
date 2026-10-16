"""Run synthetic financial-concept contrasts against the real local OMP model.

This exercises ScreeningPipeline, not the full PDF/Copilot path or a held-out
business accuracy benchmark. Requires an authenticated OMP CLI, like the existing
mandate_risk_v2_omp_server.py. OMP_TEST_MODEL can select the development model.
"""
from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.mandate_risk.catalogue import load_prebuilt_registry
from app.mandate_risk_v2.screening import ScreeningPipeline
from scripts.mandate_risk_v2_omp_server import OmpTestProvider


async def run(args) -> int:
    suite = json.loads(args.cases.read_text(encoding="utf-8"))
    cases = suite["cases"]
    if args.case_id:
        unknown = set(args.case_id) - {case["id"] for case in cases}
        if unknown:
            raise ValueError(f"unknown contrast IDs: {sorted(unknown)}")
        cases = [case for case in cases if case["id"] in args.case_id]
    args.report_dir.mkdir(parents=True, exist_ok=True)
    registry = load_prebuilt_registry()
    summaries = []
    for index, case in enumerate(cases, 1):
        result, usage = await ScreeningPipeline().run(
            document_name=f"{case['id']}.synthetic", document_text=case["text"],
            registry=registry, provider=OmpTestProvider(),
        )
        selected = sorted(item.metric.raw_row_id for item in result.screened_metrics)
        expected = sorted(case["expected_ids"])
        summary = {"id": case["id"], "expected": expected, "selected": selected,
                   "pass": selected == expected, "usage": usage}
        # Numeric filenames keep fixture IDs out of filesystem paths.
        (args.report_dir / f"case-{index:02d}.json").write_text(json.dumps(
            {"case": case, "result": result.model_dump(), "summary": summary},
            ensure_ascii=False, indent=2,
        ) + "\n", encoding="utf-8")
        summaries.append(summary)
        print(json.dumps(summary, ensure_ascii=False), flush=True)
    report = {"annotation_status": suite["annotation_status"],
              "scope": "synthetic_screening_semantics_not_pdf_or_copilot_e2e",
              "passed": sum(item["pass"] for item in summaries),
              "total": len(summaries), "cases": summaries}
    (args.report_dir / "summary.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    print(json.dumps({key: report[key] for key in ("scope", "passed", "total")}), flush=True)
    return 0 if all(item["pass"] for item in summaries) else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, default=ROOT / "tests/fixtures/mandate_recognition_contrasts.json")
    parser.add_argument("--report-dir", type=Path, required=True)
    parser.add_argument("--case-id", action="append")
    return asyncio.run(run(parser.parse_args()))


if __name__ == "__main__":
    raise SystemExit(main())
