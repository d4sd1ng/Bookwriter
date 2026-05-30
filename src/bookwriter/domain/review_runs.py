from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ReadingSampleFocus(StrEnum):
    ERROR_CORRECTION = "fehlerkorrektur"
    LOGIC_ERRORS = "logikfehler"
    TENSION_ARC = "spannungsbogen"
    WRITING_STYLE = "schreibstil"
    GRAMMAR = "grammatik"


READING_SAMPLE_SEQUENCE = [
    ReadingSampleFocus.ERROR_CORRECTION,
    ReadingSampleFocus.LOGIC_ERRORS,
    ReadingSampleFocus.TENSION_ARC,
    ReadingSampleFocus.WRITING_STYLE,
    ReadingSampleFocus.GRAMMAR,
]


@dataclass(frozen=True, slots=True)
class ReadingSampleRun:
    number: int
    focus: ReadingSampleFocus
    scope: str = "chapter"
    required: bool = True


def required_reading_sample_runs() -> list[ReadingSampleRun]:
    return [
        ReadingSampleRun(number=index + 1, focus=focus, scope="chapter")
        for index, focus in enumerate(READING_SAMPLE_SEQUENCE)
    ]
