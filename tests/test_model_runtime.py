from __future__ import annotations

import json

from bookwriter.agents.orchestrator import Orchestrator
from bookwriter.domain.models import Interview
from bookwriter.domain.model_profiles import load_model_profiles
from bookwriter.domain.review_runs import READING_SAMPLE_SEQUENCE
from bookwriter.domain.status import ApprovalStatus
from bookwriter.domain.token_usage import TokenUsageLedger
from bookwriter.runtime.model_runtime import ModelInvocation, ModelOutput
from bookwriter.runtime.ollama_runtime import ModelRuntimeBlocked, OllamaRuntime


class FakeReviewRuntime:
    enabled = True

    def __init__(self) -> None:
        self.invocation: ModelInvocation | None = None

    def invoke(self, invocation: ModelInvocation) -> ModelOutput:
        self.invocation = invocation
        return ModelOutput(
            text=json.dumps(
                {
                    "kapitelnummer": 1,
                    "fokus": "fehlerkorrektur",
                    "run_nummer": 1,
                    "erkannte_probleme": [
                        {
                            "stelle": "Absatz 1",
                            "problem": "Doppelte Aussage",
                            "korrektur": "Einen Satz streichen",
                            "prioritaet": "mittel",
                        }
                    ],
                    "aenderungsvorschlaege": ["Absatz verdichten."],
                    "restrisiken": [],
                    "blocker": [],
                }
            ),
            model="gpt-oss:20b",
            input_tokens=100,
            output_tokens=25,
        )


class FakeOllamaRuntime(OllamaRuntime):
    def __init__(self, ledger: TokenUsageLedger) -> None:
        super().__init__(profiles=load_model_profiles(), ledger=ledger)
        self.body: dict[str, object] | None = None

    def _post_generate(self, body: dict[str, object]) -> dict[str, object]:
        self.body = body
        return {
            "response": json.dumps({"status": "pending_review"}),
            "prompt_eval_count": 12,
            "eval_count": 4,
        }


class BlockingRuntime:
    enabled = True

    def invoke(self, invocation: ModelInvocation) -> ModelOutput:
        raise ModelRuntimeBlocked(["Review model does not fit the chapter context."])


class InvalidJsonRuntime:
    enabled = True

    def invoke(self, invocation: ModelInvocation) -> ModelOutput:
        return ModelOutput(
            text="not json",
            model="gpt-oss:20b",
            input_tokens=10,
            output_tokens=5,
        )


def test_model_backed_chapter_review_uses_text_analysis_prompt() -> None:
    runtime = FakeReviewRuntime()
    orchestrator = Orchestrator(model_runtime=runtime)
    project = _outlined_project(orchestrator)
    project = orchestrator.prepare_chapter_briefing(project, 1)
    project = orchestrator.approve_chapter_briefing(project, 1)
    project = orchestrator.draft_chapter(project, 1)

    updated = orchestrator.review_chapter(project, 1, READING_SAMPLE_SEQUENCE[0])

    assert runtime.invocation is not None
    assert runtime.invocation.task == "reading_sample_review"
    assert runtime.invocation.agent == "text_analysis"
    assert runtime.invocation.run_focus == "fehlerkorrektur"
    assert updated.chapter_reviews[-1].status == ApprovalStatus.PENDING_REVIEW
    assert "Doppelte Aussage" in updated.chapter_reviews[-1].findings[0]


def test_model_backed_review_blockers_are_project_blockers() -> None:
    orchestrator = Orchestrator(model_runtime=BlockingRuntime())
    project = _outlined_project(orchestrator)
    project = orchestrator.prepare_chapter_briefing(project, 1)
    project = orchestrator.approve_chapter_briefing(project, 1)
    project = orchestrator.draft_chapter(project, 1)

    updated = orchestrator.review_chapter(project, 1, READING_SAMPLE_SEQUENCE[0])

    assert updated.status == ApprovalStatus.BLOCKED
    assert updated.blockers == ["Review model does not fit the chapter context."]


def test_invalid_model_review_json_blocks_project() -> None:
    orchestrator = Orchestrator(model_runtime=InvalidJsonRuntime())
    project = _outlined_project(orchestrator)
    project = orchestrator.prepare_chapter_briefing(project, 1)
    project = orchestrator.approve_chapter_briefing(project, 1)
    project = orchestrator.draft_chapter(project, 1)

    updated = orchestrator.review_chapter(project, 1, READING_SAMPLE_SEQUENCE[0])

    assert updated.status == ApprovalStatus.BLOCKED
    assert updated.blockers == ["Model response was not valid JSON for reading_sample_review."]


def test_ollama_runtime_logs_measured_tokens(tmp_path) -> None:
    ledger = TokenUsageLedger(path=tmp_path / "usage.jsonl")
    runtime = FakeOllamaRuntime(ledger)

    output = runtime.invoke(
        ModelInvocation(
            task="reading_sample_review",
            prompt="Bitte pruefen.",
            project_id="project-1",
            agent="text_analysis",
            chapter_number=2,
            run_focus="grammatik",
        )
    )

    records = ledger.records("project-1")
    assert output.input_tokens == 12
    assert output.output_tokens == 4
    assert len(records) == 1
    assert records[0].run_focus == "grammatik"
    assert runtime.body is not None
    assert runtime.body["format"] == "json"


def test_ollama_runtime_blocks_forbidden_review_model(tmp_path) -> None:
    runtime = FakeOllamaRuntime(TokenUsageLedger(path=tmp_path / "usage.jsonl"))

    try:
        runtime.invoke(
            ModelInvocation(
                task="reading_sample_review",
                prompt="Text",
                model="qwen2.5:7b",
            )
        )
    except ModelRuntimeBlocked as error:
        assert "forbidden" in str(error)
    else:
        raise AssertionError("Forbidden review model was not blocked.")


def _interview() -> Interview:
    return Interview(
        topic="AI for consultants",
        target_audience="Independent consultants",
        book_type="Practical guide",
        desired_result="build a repeatable AI advisory offer",
        tone="direct and practical",
        length_goal="8 chapters",
        export_format="Markdown",
        value_proposition="A clear offer-building path for consultants.",
        reader_problem="They know AI matters but cannot package it.",
        book_category="Sachbuch",
        age_group="Erwachsene",
        narrative_focus="handlungsorientiert",
        perspective="3. Person",
        perspective_count="eine Perspektive",
        ending_type="offenes Ende",
        publication_format="E-Book",
        character_mode="keine Figuren",
    )


def _outlined_project(orchestrator: Orchestrator):
    project = orchestrator.create_project("Guide", _interview())
    project = orchestrator.approve_concept(project)
    project.blockers = []
    project = orchestrator.prepare_plot(project)
    project = orchestrator.approve_plot(project)
    project = orchestrator.prepare_treatment(project)
    return orchestrator.approve_treatment_and_create_outline(project, chapter_count=3)
