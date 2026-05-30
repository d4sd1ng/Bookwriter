from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


@dataclass(frozen=True, slots=True)
class ModelInvocation:
    task: str
    prompt: str
    system_prompt: str = ""
    project_id: str = ""
    agent: str = ""
    chapter_number: int | None = None
    run_focus: str = ""
    model: str | None = None
    expected_json: bool = True
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ModelOutput:
    text: str
    model: str
    input_tokens: int
    output_tokens: int
    metadata: dict[str, str] = field(default_factory=dict)


class ModelRuntime(Protocol):
    enabled: bool

    def invoke(self, invocation: ModelInvocation) -> ModelOutput:
        """Run one model invocation and return text plus measured token usage."""


class DisabledModelRuntime:
    enabled = False

    def invoke(self, invocation: ModelInvocation) -> ModelOutput:
        raise RuntimeError("Model runtime is disabled.")
