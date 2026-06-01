from __future__ import annotations

import json
import tomllib
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


@dataclass(frozen=True, slots=True)
class TokenCostProfile:
    model: str
    provider: str
    input_cost_per_million: float
    output_cost_per_million: float
    currency: str
    note: str = ""


@dataclass(frozen=True, slots=True)
class TokenUsageRecord:
    project_id: str
    task: str
    model: str
    input_tokens: int
    output_tokens: int
    agent: str = ""
    chapter_number: int | None = None
    run_focus: str = ""
    request_id: str = ""
    created_at: str = ""
    currency: str = "EUR"
    estimated_cost: float = 0.0

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id or uuid4().hex[:12],
            "created_at": self.created_at or utc_now_iso(),
            "project_id": self.project_id,
            "task": self.task,
            "agent": self.agent,
            "chapter_number": self.chapter_number,
            "run_focus": self.run_focus,
            "model": self.model,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "total_tokens": self.total_tokens,
            "currency": self.currency,
            "estimated_cost": round(self.estimated_cost, 6),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TokenUsageRecord:
        return cls(
            request_id=data.get("request_id", ""),
            created_at=data.get("created_at", ""),
            project_id=data["project_id"],
            task=data["task"],
            agent=data.get("agent", ""),
            chapter_number=data.get("chapter_number"),
            run_focus=data.get("run_focus", ""),
            model=data["model"],
            input_tokens=int(data["input_tokens"]),
            output_tokens=int(data["output_tokens"]),
            currency=data.get("currency", "EUR"),
            estimated_cost=float(data.get("estimated_cost", 0.0)),
        )


@dataclass(frozen=True, slots=True)
class TokenUsageSummary:
    input_tokens: int
    output_tokens: int
    total_tokens: int
    estimated_cost: float
    currency: str
    records: int


class TokenCostCatalog:
    def __init__(self, path: Path | str = "config/token_costs.toml") -> None:
        self.path = Path(path)
        self.data = tomllib.loads(self.path.read_text(encoding="utf-8"))

    @property
    def ledger_path(self) -> Path:
        return Path(self.data["defaults"]["ledger_path"])

    def profile_for(self, model: str) -> TokenCostProfile:
        models = self.data.get("models", {})
        if model not in models:
            if self.data["defaults"].get("block_unknown_external_model_costs", True):
                raise KeyError(f"No token cost profile configured for model: {model}")
            raw = {
                "provider": "unknown",
                "api_cost_per_million_input_tokens": 0.0,
                "api_cost_per_million_output_tokens": 0.0,
                "cost_note": "No explicit cost profile.",
            }
        else:
            raw = models[model]
        return TokenCostProfile(
            model=model,
            provider=raw["provider"],
            input_cost_per_million=float(raw["api_cost_per_million_input_tokens"]),
            output_cost_per_million=float(raw["api_cost_per_million_output_tokens"]),
            currency=self.data["defaults"]["currency"],
            note=raw.get("cost_note", ""),
        )

    def estimate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        profile = self.profile_for(model)
        return (
            input_tokens * profile.input_cost_per_million
            + output_tokens * profile.output_cost_per_million
        ) / 1_000_000

    def default_external_review_run_limit(self) -> float:
        return float(self.data["defaults"].get("default_external_review_run_limit", 0.02))

    def default_external_chapter_review_limit(self) -> float:
        return float(self.data["defaults"].get("default_external_chapter_review_limit", 0.10))

    def default_external_full_chapter_limit(self) -> float:
        return float(self.data["defaults"].get("default_external_full_chapter_limit", 0.15))

    def default_external_review_completion_tokens(self) -> int:
        return int(self.data["defaults"].get("default_external_review_completion_tokens", 4096))

    def default_external_revision_completion_tokens(self) -> int:
        return int(self.data["defaults"].get("default_external_revision_completion_tokens", 8192))


class TokenUsageLedger:
    def __init__(self, path: Path | str | None = None) -> None:
        catalog = TokenCostCatalog()
        self.path = Path(path) if path else catalog.ledger_path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.catalog = catalog

    def append(self, record: TokenUsageRecord) -> TokenUsageRecord:
        estimated_cost = self.catalog.estimate_cost(
            record.model,
            record.input_tokens,
            record.output_tokens,
        )
        normalized = TokenUsageRecord(
            request_id=record.request_id or uuid4().hex[:12],
            created_at=record.created_at or utc_now_iso(),
            project_id=record.project_id,
            task=record.task,
            agent=record.agent,
            chapter_number=record.chapter_number,
            run_focus=record.run_focus,
            model=record.model,
            input_tokens=record.input_tokens,
            output_tokens=record.output_tokens,
            currency=self.catalog.profile_for(record.model).currency,
            estimated_cost=estimated_cost,
        )
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(normalized.to_dict(), ensure_ascii=False) + "\n")
        return normalized

    def records(self, project_id: str | None = None) -> list[TokenUsageRecord]:
        if not self.path.exists():
            return []
        records: list[TokenUsageRecord] = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            record = TokenUsageRecord.from_dict(json.loads(line))
            if project_id is None or record.project_id == project_id:
                records.append(record)
        return records

    def summary(self, project_id: str | None = None) -> TokenUsageSummary:
        records = self.records(project_id)
        input_tokens = sum(record.input_tokens for record in records)
        output_tokens = sum(record.output_tokens for record in records)
        estimated_cost = sum(record.estimated_cost for record in records)
        currency = records[0].currency if records else self.catalog.data["defaults"]["currency"]
        return TokenUsageSummary(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=input_tokens + output_tokens,
            estimated_cost=round(estimated_cost, 6),
            currency=currency,
            records=len(records),
        )
