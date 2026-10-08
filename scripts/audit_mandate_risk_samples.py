"""Compare saved screening results with the editable manual review baseline."""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def audit_samples():
    review = ROOT / "docs/review"
    baseline = json.loads((review / "mandate-risk-v2-samples.json").read_text())
    with (review / "mandate-risk-v2-labels.csv").open(encoding="utf-8-sig", newline="") as stream:
        labels = list(csv.DictReader(stream))
    reports = []
    for sample in baseline["samples"]:
        result = json.loads((ROOT / sample["result_path"]).read_text())
        if (result["document_name"] != sample["pdf"]
                or result["metric_catalogue_sha256"] != baseline["catalogue_sha256"]):
            raise ValueError("Sample document or catalogue differs from the review baseline")
        metrics = {item["metric"]["source_row"]: item for item in result["screened_metrics"]}
        rows = [row for row in labels if row["sample"] == sample["sample"]]
        required = [row for row in rows if row["label"] == "必选"]
        missing = [row["metric_name"] for row in required if int(row["raw_row_id"]) not in metrics]
        hidden = [row["metric_name"] for row in required if int(row["raw_row_id"]) in metrics
                  and (metrics[int(row["raw_row_id"])].get("match_score") is None
                       or metrics[int(row["raw_row_id"])]["match_score"] < 50)]
        unrelated = [row["metric_name"] for row in rows
                     if row["label"] == "无关" and int(row["raw_row_id"]) in metrics]
        scores = [item.get("match_score") for item in metrics.values()]
        reports.append({
            "pdf": sample["pdf"], "analysis_mode": result["analysis_mode"],
            "coverage_status": result["coverage_status"],
            "labels": len(rows), "required": len(required),
            "required_recalled": len(required) - len(missing),
            "required_missing": missing, "required_hidden": hidden,
            "unrelated_recalled": unrelated,
            "candidates": len(metrics), "visible_at_50": sum(s is not None and s >= 50 for s in scores),
            "weak": sum(s is not None and s < 50 for s in scores),
            "unscored": sum(s is None for s in scores),
        })
    return {"annotation_status": baseline["annotation_status"], "samples": reports}


if __name__ == "__main__":
    print(json.dumps(audit_samples(), ensure_ascii=False, indent=2))
