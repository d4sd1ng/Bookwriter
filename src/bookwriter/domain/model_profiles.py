from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class ModelTaskProfile:
    task: str
    model: str
    reasoning_effort: str
    temperature: float
    requires_structured_output: bool
    max_output_tokens: int = 2048
    minimum_context_tokens: int = 0
    preferred_context_tokens: int = 0
    requires_thinking: bool = False
    allow_secondary_model: bool = True
    allow_secondary_review_model: bool = False
    secondary_review_max_input_tokens: int = 0
    alternative_model: str = ""
    long_text_strategy: str = ""
    requires_approved_market_data: bool = False
    requires_final_approval: bool = False


@dataclass(frozen=True, slots=True)
class ModelProfiles:
    provider: str
    base_url: str
    primary_model: str
    secondary_model: str
    review_model: str
    secondary_review_model: str
    minimum_review_context_tokens: int
    preferred_review_context_tokens: int
    forbid_secondary_model_for_reviews: bool
    allow_secondary_review_model_for_short_reviews: bool
    model_context_tokens: dict[str, int]
    blocked_models: dict[str, str]
    tasks: dict[str, ModelTaskProfile]


def load_model_profiles(path: Path | str = "config/model_profiles.toml") -> ModelProfiles:
    data = tomllib.loads(Path(path).read_text(encoding="utf-8"))
    default = data["default"]
    tasks: dict[str, ModelTaskProfile] = {}
    for task_name, raw_profile in data["tasks"].items():
        profile: dict[str, Any] = raw_profile
        tasks[task_name] = ModelTaskProfile(
            task=task_name,
            model=profile["model"],
            reasoning_effort=profile["reasoning_effort"],
            temperature=float(profile["temperature"]),
            requires_structured_output=bool(profile["requires_structured_output"]),
            max_output_tokens=int(profile.get("max_output_tokens", 2048)),
            minimum_context_tokens=int(profile.get("minimum_context_tokens", 0)),
            preferred_context_tokens=int(profile.get("preferred_context_tokens", 0)),
            requires_thinking=bool(profile.get("requires_thinking", False)),
            allow_secondary_model=bool(profile.get("allow_secondary_model", True)),
            allow_secondary_review_model=bool(profile.get("allow_secondary_review_model", False)),
            secondary_review_max_input_tokens=int(profile.get("secondary_review_max_input_tokens", 0)),
            alternative_model=str(profile.get("alternative_model", "")),
            long_text_strategy=str(profile.get("long_text_strategy", "")),
            requires_approved_market_data=bool(profile.get("requires_approved_market_data", False)),
            requires_final_approval=bool(profile.get("requires_final_approval", False)),
        )
    model_context_tokens: dict[str, int] = {
        default["primary_model"]: int(default["preferred_review_context_tokens"]),
        default["review_model"]: int(default["preferred_review_context_tokens"]),
    }
    for candidate in data.get("candidate_models", []):
        if candidate.get("context_tokens"):
            model_context_tokens[str(candidate["name"])] = int(candidate["context_tokens"])
    blocked_models = {
        model: str(health.get("reason", "Model is not approved for runtime."))
        for model, health in data.get("model_health", {}).items()
        if not bool(health.get("approved_for_runtime", True))
    }
    return ModelProfiles(
        provider=default["provider"],
        base_url=default["base_url"],
        primary_model=default["primary_model"],
        secondary_model=default["secondary_model"],
        review_model=default["review_model"],
        secondary_review_model=default["secondary_review_model"],
        minimum_review_context_tokens=int(default["minimum_review_context_tokens"]),
        preferred_review_context_tokens=int(default["preferred_review_context_tokens"]),
        forbid_secondary_model_for_reviews=bool(default["forbid_secondary_model_for_reviews"]),
        allow_secondary_review_model_for_short_reviews=bool(
            default["allow_secondary_review_model_for_short_reviews"]
        ),
        model_context_tokens=model_context_tokens,
        blocked_models=blocked_models,
        tasks=tasks,
    )
