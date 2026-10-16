"""Evaluate document/metric recognition, not portfolio values or legal compliance.

Example: python scripts/evaluate_mandate_recognition.py --result run.json \
  --gold tests/fixtures/mandate_recognition_equity.json --pdf equity.pdf --output evaluation.json
Multiple --result inputs additionally report selected-set stability. Gold labels
are never loaded by the production recognition pipeline.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re


def _normalise(text: str) -> str:
    text = text.replace("\u2010", "-").replace("\u2011", "-")
    text = re.sub(r"(?<=\w)-\s+(?=\w)", "-", text)
    return " ".join(text.split())


def _result(payload: dict) -> dict:
    if payload.get("event") == "run.failed":
        raise ValueError("cannot evaluate a failed run as an empty successful result")
    if "metadata" in payload:
        payload = payload["metadata"].get("mandate_risk_v2", {}).get("result")
    elif "structured_result" in payload:
        payload = payload["structured_result"]
    if not isinstance(payload, dict) or not any(
        key in payload for key in ("screened_metrics", "matched_metrics", "candidate_metrics")
    ):
        raise ValueError("missing structured recognition result")
    return payload


def _counts(selected: set[int], positive: set[int], negative: set[int]) -> dict:
    tp, fp, fn = selected & positive, selected & negative, positive - selected
    denominator = 2 * len(tp) + len(fp) + len(fn)
    return {
        "tp": len(tp), "fp": len(fp), "fn": len(fn),
        "precision": len(tp) / (len(tp) + len(fp)) if tp or fp else None,
        "recall": len(tp) / len(positive) if positive else None,
        "f1": 2 * len(tp) / denominator if denominator else None,
        "true_positive_ids": sorted(tp), "false_positive_ids": sorted(fp),
        "false_negative_ids": sorted(fn),
    }


def evaluate(payload: dict, gold: dict, *, pdf_pages: dict[int, str] | None = None) -> dict:
    result = _result(payload)
    annotations = gold["annotations"]
    ids = [item["raw_row_id"] for item in annotations]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate gold metric identity")
    if any(item["expected"] not in {"MATCH", "NO_MATCH", "NEEDS_ADJUDICATION"} for item in annotations):
        raise ValueError("unknown gold decision")
    labels = {item["raw_row_id"]: item for item in annotations}
    expected_sha = gold.get("catalogue_sha256")
    actual_sha = result.get("metric_catalogue_sha256")
    if expected_sha and actual_sha and expected_sha != actual_sha:
        raise ValueError("catalogue changed: re-adjudicate the baseline before evaluating")
    expected_name = gold.get("document", {}).get("name")
    if expected_name and result.get("document_name") != expected_name:
        raise ValueError("result document name differs from the baseline")
    rows = result.get("screened_metrics")
    if rows is None:
        rows = [*result.get("matched_metrics", []), *result.get("candidate_metrics", [])]
    selected, direct, review, unclassified = set(), set(), set(), set()
    evidence_checks = []
    for item in rows:
        metric = item["metric"]
        row_id = metric["raw_row_id"]
        if row_id not in labels:
            raise ValueError(f"unlabelled metric identity: {row_id}")
        label = labels[row_id]
        if (metric["metric_name"] != label["metric_name"]
                or ("algorithm" in label and metric.get("algorithm") != label["algorithm"])):
            raise ValueError(f"catalogue metric changed: {row_id}")
        selected.add(row_id)
        associations = item.get("requirements", [])
        if not associations:
            unclassified.add(row_id)
            evidence_checks.append({"raw_row_id": row_id, "status": "MISSING_EVIDENCE"})
        anchors = [gold["evidence_sources"][key] for key in label.get("evidence_ids", [])]
        for association in associations:
            level = association.get("mapping_level")
            if level == "DIRECT":
                direct.add(row_id)
            elif level == "REVIEW":
                review.add(row_id)
            else:
                unclassified.add(row_id)
            evidence = association.get("mapping_evidence", [])
            if not evidence or any(not quote.get("text") or not quote.get("clause_id")
                                   or not isinstance(quote.get("page"), int) for quote in evidence):
                status = "MISSING_EVIDENCE"
            elif pdf_pages is None:
                status = "UNVERIFIED_WITHOUT_PDF"
            elif any(_normalise(quote["text"]) not in _normalise(pdf_pages.get(quote["page"], ""))
                     for quote in evidence):
                status = "SOURCE_MISMATCH"
            elif anchors and not any(
                quote["page"] == anchor["page"]
                and _normalise(anchor["quote"]) in _normalise(quote["text"])
                for quote in evidence for anchor in anchors
            ):
                status = "BASELINE_ANCHOR_NOT_CITED"
            else:
                status = "SOURCE_AND_ANCHOR_VERIFIED"
            evidence_checks.append({"raw_row_id": row_id,
                                    "requirement_id": association.get("requirement", {}).get("requirement", {}).get("requirement_id"),
                                    "status": status})
    positive = {row_id for row_id, item in labels.items() if item["expected"] == "MATCH"}
    negative = {row_id for row_id, item in labels.items() if item["expected"] == "NO_MATCH"}
    ambiguous = set(labels) - positive - negative
    return {
        "annotation_status": gold.get("annotation_status", "unspecified"),
        "scope": gold.get("scope", "unspecified"),
        "document_name": result.get("document_name"),
        "catalogue_identity_verified": bool(expected_sha and actual_sha),
        "selected_ids": sorted(selected),
        "combined": _counts(selected, positive, negative),
        "direct": _counts(direct, positive, negative),
        "review": _counts(review, positive, negative),
        "unclassified_selected_ids": sorted(unclassified),
        "needs_adjudication_ids": sorted(ambiguous),
        "selected_needs_adjudication_ids": sorted(selected & ambiguous),
        "evidence_status_counts": dict(Counter(item["status"] for item in evidence_checks)),
        "evidence_checks": evidence_checks,
        "limits": ["开发集初标结果不代表业务审核、跨文档准确率或合规结论。",
                   "DIRECT/REVIEW分项不能代替合并指标，防止通过重分类隐藏误报。",
                   "证据校验仅验证出处和初标锚点，不自动证明语义蕴含或数值/条件完整性。"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--result", type=Path, action="append", required=True)
    parser.add_argument("--gold", type=Path, required=True)
    parser.add_argument("--pdf", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    gold = json.loads(args.gold.read_text(encoding="utf-8"))
    pages = None
    if args.pdf:
        raw = args.pdf.read_bytes()
        expected_sha = gold.get("document", {}).get("sha256")
        if not expected_sha or hashlib.sha256(raw).hexdigest() != expected_sha:
            parser.error("PDF hash differs from the baseline or baseline hash is absent")
        from pypdf import PdfReader
        pages = {index: page.extract_text() or "" for index, page in enumerate(PdfReader(args.pdf).pages, 1)}
    reports = [{"input": str(path), **evaluate(
        json.loads(path.read_text(encoding="utf-8")), gold, pdf_pages=pages,
    )} for path in args.result]
    comparisons = []
    for index, left in enumerate(reports):
        a = set(left["selected_ids"])
        for right in reports[index + 1:]:
            b = set(right["selected_ids"])
            comparisons.append({"left": left["input"], "right": right["input"],
                                "jaccard": len(a & b) / len(a | b) if a | b else 1.0,
                                "only_left": sorted(a - b), "only_right": sorted(b - a)})
    output = {"reports": reports, "selected_set_comparisons": comparisons}
    encoded = json.dumps(output, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded + "\n", encoding="utf-8")
    print(encoded)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
