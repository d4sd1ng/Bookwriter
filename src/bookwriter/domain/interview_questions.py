from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class InterviewQuestion:
    field: str
    label: str
    prompt: str
    required: bool
    stage: str
    blocks_if_missing: bool = False


def load_interview_questions(
    path: Path | str = "config/interview_questions.toml",
) -> list[InterviewQuestion]:
    data = tomllib.loads(Path(path).read_text(encoding="utf-8"))
    return [InterviewQuestion(**question) for question in data["questions"]]


def question_by_field(field: str) -> InterviewQuestion | None:
    for question in load_interview_questions():
        if question.field == field:
            return question
    return None
