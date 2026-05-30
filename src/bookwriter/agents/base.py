from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

from bookwriter.domain.status import ApprovalStatus

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class AgentResult(Generic[T]):
    agent: str
    output: T
    status: ApprovalStatus
    notes: list[str]
