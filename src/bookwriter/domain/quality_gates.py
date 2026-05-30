from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class QualityGateResult:
    ok: bool
    blockers: list[str]
    minimum_score: float
    actual_score: float


def evaluate_quality_score(
    task: str,
    actual_score: float,
    path: Path | str = "config/quality_gates.toml",
) -> QualityGateResult:
    data = tomllib.loads(Path(path).read_text(encoding="utf-8"))
    task_config = data.get("tasks", {}).get(task, {})
    minimum_score = float(task_config.get("minimum_total_score", data["defaults"]["minimum_total_score"]))
    blockers: list[str] = []
    if actual_score < minimum_score and data["defaults"].get("block_below_minimum", True):
        blockers.append(
            f"Quality score below gate for {task}: {actual_score:.2f} < {minimum_score:.2f}."
        )
    return QualityGateResult(
        ok=not blockers,
        blockers=blockers,
        minimum_score=minimum_score,
        actual_score=actual_score,
    )
