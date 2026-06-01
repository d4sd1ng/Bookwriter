from __future__ import annotations

from bookwriter.cli import main
from bookwriter.domain.token_usage import TokenCostCatalog, TokenUsageLedger, TokenUsageRecord


def test_local_ollama_models_have_zero_api_cost() -> None:
    catalog = TokenCostCatalog()

    assert catalog.estimate_cost("gpt-oss:20b", input_tokens=10_000, output_tokens=2_000) == 0
    assert catalog.estimate_cost("qwen3:14b", input_tokens=10_000, output_tokens=2_000) == 0


def test_external_openai_model_cost_profile_is_configured() -> None:
    catalog = TokenCostCatalog()

    assert catalog.profile_for("gpt-5-mini").provider == "openai"
    assert catalog.estimate_cost("gpt-5-mini", input_tokens=10_000, output_tokens=2_000) == 0.0065
    assert catalog.default_external_review_run_limit() == 0.02
    assert catalog.default_external_chapter_review_limit() == 0.10
    assert catalog.default_external_review_completion_tokens() == 4096
    assert catalog.default_external_revision_completion_tokens() == 8192


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


def test_usage_command_shows_default_external_review_budgets(capsys) -> None:
    assert main(["usage", "--project-id", "missing-project"]) == 0

    output = capsys.readouterr().out
    assert "Default external review run limit: 0.02 USD" in output
    assert "Default external chapter review budget: 0.10 USD" in output
    assert "Default external review completion tokens: 4096" in output
    assert "Default external revision completion tokens: 8192" in output
