from __future__ import annotations

from bookwriter.domain.review_runs import ReadingSampleFocus, required_reading_sample_runs


def test_each_chapter_requires_five_separate_reading_sample_runs() -> None:
    runs = required_reading_sample_runs()

    assert [run.focus for run in runs] == [
        ReadingSampleFocus.ERROR_CORRECTION,
        ReadingSampleFocus.LOGIC_ERRORS,
        ReadingSampleFocus.TENSION_ARC,
        ReadingSampleFocus.WRITING_STYLE,
        ReadingSampleFocus.GRAMMAR,
    ]
    assert [run.number for run in runs] == [1, 2, 3, 4, 5]
    assert {run.scope for run in runs} == {"chapter"}
    assert all(run.required for run in runs)
