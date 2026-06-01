from __future__ import annotations

from bookwriter.domain.token_usage import TokenCostCatalog, TokenUsageLedger, TokenUsageRecord


def test_local_ollama_models_have_zero_api_cost() -> None:
    catalog = TokenCostCatalog()

    assert catalog.estimate_cost("gpt-oss:20b", input_tokens=10_000, output_tokens=2_000) == 0
    assert catalog.estimate_cost("qwen3:14b", input_tokens=10_000, output_tokens=2_000) == 0


def test_external_openai_model_cost_profile_is_configured() -> None:
    catalog = TokenCostCatalog()

    assert catalog.profile_for("gpt-5-mini").provider == "openai"
    assert catalog.estimate_cost("gpt-5-mini", input_tokens=10_000, output_tokens=2_000) == 0.0065


def test_token_usage_ledger_summarizes_project_usage(tmp_path) -> None:
    ledger = TokenUsageLedger(path=tmp_path / "usage.jsonl")
    ledger.append(
        TokenUsageRecord(
            project_id="project-a",
            task="reading_sample_review",
            model="gpt-oss:20b",
            input_tokens=1200,
            output_tokens=300,
            chapter_number=1,
            run_focus="logikfehler",
        )
    )
    ledger.append(
        TokenUsageRecord(
            project_id="project-b",
            task="outline",
            model="gpt-oss:20b",
            input_tokens=500,
            output_tokens=200,
        )
    )

    summary = ledger.summary(project_id="project-a")

    assert summary.records == 1
    assert summary.input_tokens == 1200
    assert summary.output_tokens == 300
    assert summary.total_tokens == 1500
    assert summary.estimated_cost == 0
