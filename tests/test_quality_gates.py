from __future__ import annotations

from bookwriter.domain.quality_gates import evaluate_quality_score


def test_review_quality_gate_blocks_low_scores() -> None:
    result = evaluate_quality_score("reading_sample_review", actual_score=4.0)

    assert result.ok is False
    assert result.blockers


def test_review_quality_gate_accepts_good_scores() -> None:
    result = evaluate_quality_score("reading_sample_review", actual_score=4.6)

    assert result.ok is True
    assert not result.blockers
