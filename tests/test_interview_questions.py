from __future__ import annotations

from bookwriter.domain.interview_questions import load_interview_questions, question_by_field


def test_interview_questionnaire_contains_required_contract_fields() -> None:
    questions = load_interview_questions()
    required_fields = {question.field for question in questions if question.required}

    assert "target_audience" in required_fields
    assert "reader_problem" in required_fields
    assert "value_proposition" in required_fields
    assert "book_type" in required_fields
    assert "export_format" in required_fields


def test_question_lookup_returns_prompt() -> None:
    question = question_by_field("target_audience")

    assert question is not None
    assert question.blocks_if_missing is True
