from __future__ import annotations

from bookwriter.domain.model_profiles import load_model_profiles
from bookwriter.domain.model_selection import select_model_for_task


def test_model_profiles_define_primary_and_secondary_models() -> None:
    profiles = load_model_profiles()

    assert profiles.primary_model == "gpt-oss:20b"
    assert profiles.secondary_model == "qwen2.5:7b"
    assert profiles.review_model == "gpt-oss:20b"
    assert profiles.secondary_review_model == "qwen3:14b"


def test_model_profiles_route_sensitive_tasks_to_primary_model() -> None:
    profiles = load_model_profiles()

    assert profiles.tasks["orchestration"].model == "gpt-oss:20b"
    assert profiles.tasks["market_assessment"].requires_approved_market_data is True
    assert profiles.tasks["kdp_preparation"].requires_final_approval is True


def test_review_tasks_require_review_model_and_large_context() -> None:
    profiles = load_model_profiles()

    for task in ["editing", "reading_sample_review", "consistency_review"]:
        profile = profiles.tasks[task]
        assert profile.model == profiles.review_model
        assert profile.allow_secondary_model is False
        assert profile.minimum_context_tokens >= 32768
        assert profile.requires_thinking is True


def test_secondary_model_is_blocked_for_review_tasks() -> None:
    profiles = load_model_profiles()

    result = select_model_for_task(
        profiles,
        "reading_sample_review",
        available_context_tokens=32768,
        requested_model=profiles.secondary_model,
    )

    assert result.ok is False
    assert result.blockers


def test_secondary_review_model_profile_allows_short_chapter_reviews_but_health_blocks_runtime() -> None:
    profiles = load_model_profiles()

    result = select_model_for_task(
        profiles,
        "reading_sample_review",
        available_context_tokens=40960,
        input_tokens=18000,
        requested_model=profiles.secondary_review_model,
    )

    assert result.ok is False
    assert result.model == "qwen3:14b"
    assert any("health check" in blocker for blocker in result.blockers)


def test_secondary_review_model_blocks_long_chapter_reviews() -> None:
    profiles = load_model_profiles()

    result = select_model_for_task(
        profiles,
        "reading_sample_review",
        available_context_tokens=40960,
        input_tokens=36000,
        requested_model=profiles.secondary_review_model,
    )

    assert result.ok is False
    assert any("short review" in blocker for blocker in result.blockers)


def test_review_task_blocks_when_context_is_too_small() -> None:
    profiles = load_model_profiles()

    result = select_model_for_task(
        profiles,
        "consistency_review",
        available_context_tokens=32768,
    )

    assert result.ok is False
    assert any("context" in blocker.lower() for blocker in result.blockers)


def test_broken_primary_review_model_is_blocked_by_local_health_check() -> None:
    profiles = load_model_profiles()

    result = select_model_for_task(
        profiles,
        "reading_sample_review",
        available_context_tokens=131072,
        requested_model="gpt-oss:20b",
    )

    assert result.ok is False
    assert any("gpt-oss:20b" in blocker and "health check" in blocker for blocker in result.blockers)
