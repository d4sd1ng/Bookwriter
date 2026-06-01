from __future__ import annotations

import json

from bookwriter.domain.model_profiles import load_model_profiles
from bookwriter.domain.token_usage import TokenUsageLedger
from bookwriter.runtime.model_runtime import ModelInvocation
from bookwriter.runtime.ollama_runtime import ModelRuntimeBlocked
from bookwriter.runtime.openai_runtime import OpenAIChatRuntime


class FakeOpenAIRuntime(OpenAIChatRuntime):
    def __init__(self, ledger: TokenUsageLedger) -> None:
        super().__init__(profiles=load_model_profiles(), ledger=ledger)
        self.body: dict[str, object] | None = None

    def _post_chat(self, body: dict[str, object], api_key: str) -> dict[str, object]:
        self.body = body
        return {
            "model": "gpt-5-mini",
            "choices": [
                {
                    "message": {
                        "content": json.dumps(
                            {
                                "status": "pending_review",
                                "blocker": [],
                                "erkannte_probleme": [],
                            }
                        )
                    }
                }
            ],
            "usage": {
                "prompt_tokens": 120,
                "completion_tokens": 30,
                "total_tokens": 150,
            },
        }


def test_openai_runtime_logs_measured_tokens_and_costs(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    ledger = TokenUsageLedger(path=tmp_path / "usage.jsonl")
    runtime = FakeOpenAIRuntime(ledger)

    output = runtime.invoke(
        ModelInvocation(
            task="reading_sample_review",
            prompt="Bitte JSON pruefen.",
            project_id="project-1",
            agent="text_analysis",
            chapter_number=1,
            run_focus="fehlerkorrektur",
            model="gpt-5-mini",
        )
    )

    records = ledger.records("project-1")
    assert output.input_tokens == 120
    assert output.output_tokens == 30
    assert output.metadata["estimated_cost"] == "0.000090"
    assert output.metadata["currency"] == "USD"
    assert records[0].model == "gpt-5-mini"
    assert records[0].estimated_cost == 0.00009
    assert runtime.body is not None
    assert runtime.body["response_format"] == {"type": "json_object"}
    assert runtime.body["max_completion_tokens"] == 768


def test_openai_runtime_blocks_unknown_external_cost_profile(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    runtime = FakeOpenAIRuntime(TokenUsageLedger(path=tmp_path / "usage.jsonl"))

    try:
        runtime.invoke(
            ModelInvocation(
                task="reading_sample_review",
                prompt="Bitte JSON pruefen.",
                model="unknown-external-model",
            )
        )
    except ModelRuntimeBlocked as error:
        assert "No token cost profile" in str(error)
    else:
        raise AssertionError("Unknown external model cost profile was not blocked.")


def test_openai_runtime_blocks_when_api_key_is_missing(tmp_path, monkeypatch) -> None:
    monkeypatch.delenv("BOOKWRITER_TEST_MISSING_KEY", raising=False)
    runtime = FakeOpenAIRuntime(TokenUsageLedger(path=tmp_path / "usage.jsonl"))
    runtime.api_key_env = "BOOKWRITER_TEST_MISSING_KEY"

    try:
        runtime.invoke(
            ModelInvocation(
                task="reading_sample_review",
                prompt="Bitte JSON pruefen.",
                model="gpt-5-mini",
            )
        )
    except ModelRuntimeBlocked as error:
        assert "BOOKWRITER_TEST_MISSING_KEY" in str(error)
    else:
        raise AssertionError("Missing API key was not blocked.")


def test_openai_runtime_blocks_when_estimated_cost_exceeds_limit(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    runtime = FakeOpenAIRuntime(TokenUsageLedger(path=tmp_path / "usage.jsonl"))
    runtime.max_estimated_cost = 0.000001

    try:
        runtime.invoke(
            ModelInvocation(
                task="reading_sample_review",
                prompt="Bitte JSON pruefen.",
                model="gpt-5-mini",
            )
        )
    except ModelRuntimeBlocked as error:
        assert "exceeds configured run limit" in str(error)
    else:
        raise AssertionError("Estimated cost limit was not enforced.")


def test_openai_runtime_uses_default_review_budget(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    runtime = FakeOpenAIRuntime(TokenUsageLedger(path=tmp_path / "usage.jsonl"))

    runtime.invoke(
        ModelInvocation(
            task="reading_sample_review",
            prompt="Bitte JSON pruefen.",
            model="gpt-5-mini",
        )
    )

    assert runtime.body is not None
