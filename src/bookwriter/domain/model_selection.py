from __future__ import annotations

from dataclasses import dataclass

from bookwriter.domain.model_profiles import ModelProfiles, ModelTaskProfile


REVIEW_TASKS = {"editing", "reading_sample_review", "consistency_review"}


@dataclass(frozen=True, slots=True)
class ModelSelectionResult:
    ok: bool
    model: str
    blockers: list[str]
    long_text_strategy: str


def select_model_for_task(
    profiles: ModelProfiles,
    task: str,
    available_context_tokens: int,
    input_tokens: int = 0,
    requested_model: str | None = None,
) -> ModelSelectionResult:
    profile = profiles.tasks[task]
    model = requested_model or profile.model
    blockers = _validate_review_model(profiles, profile, model, available_context_tokens, input_tokens)
    return ModelSelectionResult(
        ok=not blockers,
        model=model,
        blockers=blockers,
        long_text_strategy=profile.long_text_strategy,
    )


def _validate_review_model(
    profiles: ModelProfiles,
    profile: ModelTaskProfile,
    model: str,
    available_context_tokens: int,
    input_tokens: int,
) -> list[str]:
    if profile.task not in REVIEW_TASKS:
        return []

    blockers: list[str] = []
    if (
        profiles.allow_secondary_review_model_for_short_reviews
        and profile.allow_secondary_review_model
        and model == profiles.secondary_review_model
    ):
        if input_tokens and input_tokens > profile.secondary_review_max_input_tokens:
            blockers.append(
                "Secondary review model is only allowed for short review inputs: "
                f"{input_tokens} > {profile.secondary_review_max_input_tokens}."
            )
        if available_context_tokens < profile.minimum_context_tokens:
            blockers.append(
                "Available context window is below the minimum for this review task: "
                f"{available_context_tokens} < {profile.minimum_context_tokens}."
            )
        return blockers

    if profiles.forbid_secondary_model_for_reviews and model == profiles.secondary_model:
        blockers.append("Secondary model is forbidden for review tasks.")
    if not profile.allow_secondary_model and model != profiles.review_model:
        blockers.append(f"Review task requires review model: {profiles.review_model}.")
    if available_context_tokens < profile.minimum_context_tokens:
        blockers.append(
            "Available context window is below the minimum for this review task: "
            f"{available_context_tokens} < {profile.minimum_context_tokens}."
        )
    return blockers
