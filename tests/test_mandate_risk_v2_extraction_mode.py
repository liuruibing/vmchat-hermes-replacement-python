from app.mandate_risk.clauses import split_document_clauses
from app.mandate_risk_v2.pipeline import choose_extraction_windows


def _document(paragraphs: int) -> str:
    return "[Page 1]\n" + "\n\n".join(
        f"Requirement {index}: the portfolio shall maintain condition {index}."
        for index in range(1, paragraphs + 1)
    )


def test_normal_mandate_prefers_one_global_semantic_read():
    clauses = split_document_clauses(_document(12))
    mode, windows = choose_extraction_windows(
        clauses,
        batch_size=6,
        overlap=2,
        full_document_max_clauses=20,
        full_document_max_chars=100_000,
    )

    assert mode == "full_document"
    assert len(windows) == 1
    assert [item.clause_id for item in windows[0]] == [item.clause_id for item in clauses]


def test_long_mandate_falls_back_to_overlapping_windows():
    clauses = split_document_clauses(_document(14))
    mode, windows = choose_extraction_windows(
        clauses,
        batch_size=6,
        overlap=2,
        full_document_max_clauses=8,
        full_document_max_chars=100_000,
    )

    assert mode == "chunked"
    assert len(windows) > 1
    assert windows[0][-2].clause_id == windows[1][0].clause_id
    assert windows[0][-1].clause_id == windows[1][1].clause_id


def test_character_limit_can_force_chunking():
    clauses = split_document_clauses(
        "[Page 1]\n" + ("The portfolio shall maintain prudent liquidity. " * 100)
    )
    mode, windows = choose_extraction_windows(
        clauses,
        batch_size=4,
        overlap=1,
        full_document_max_clauses=200,
        full_document_max_chars=100,
    )

    assert len(clauses) <= 200  # clause count alone would permit a full-document read
    assert mode == "chunked"    # character limit independently forces the fallback
    assert len(windows) > 1


def test_default_budget_reads_many_short_clauses_together():
    clauses = split_document_clauses(_document(150))
    mode, windows = choose_extraction_windows(clauses)
    assert mode == "full_document"
    assert len(windows[0]) == len(clauses)
