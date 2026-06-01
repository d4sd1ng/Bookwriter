from __future__ import annotations

import json
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from bookwriter.agents.chapter_agent import ChapterReviewAgent
from bookwriter.domain.models import BookProject, ChapterDraft, Interview
from bookwriter.domain.review_runs import READING_SAMPLE_SEQUENCE, ReadingSampleFocus
from bookwriter.runtime.model_runtime import ModelRuntime


@dataclass(frozen=True, slots=True)
class ReadingSampleBenchmarkCase:
    case_id: str
    book_name: str
    topic: str
    target_audience: str
    book_type: str
    book_category: str
    age_group: str
    narrative_focus: str
    perspective: str
    tone: str
    chapter_number: int
    chapter_title: str
    chapter_goal: str
    chapter_markdown: str


def load_reading_sample_cases(
    path: Path | str = "benchmarks/reading_sample_cases.toml",
) -> list[ReadingSampleBenchmarkCase]:
    data = tomllib.loads(Path(path).read_text(encoding="utf-8"))
    return [ReadingSampleBenchmarkCase(**raw_case) for raw_case in data.get("cases", [])]


def run_reading_sample_benchmark(
    runtime: ModelRuntime,
    cases: list[ReadingSampleBenchmarkCase],
    focus: ReadingSampleFocus | None = None,
    model: str | None = None,
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    focuses = [focus] if focus else list(READING_SAMPLE_SEQUENCE)
    for case in cases:
        for current_focus in focuses:
            project = _project_from_case(case)
            draft = _draft_from_case(case)
            agent = ChapterReviewAgent(model_runtime=runtime, requested_model=model)
            result = agent.run(project, draft, current_focus)
            model_output = agent.last_model_output
            results.append(
                {
                    "case_id": case.case_id,
                    "focus": current_focus.value,
                    "status": result.output.status.value,
                    "findings": len(result.output.findings),
                    "finding_details": result.output.findings,
                    "change_suggestions": len(result.output.change_suggestions),
                    "change_suggestion_details": result.output.change_suggestions,
                    "residual_risks": result.output.residual_risks,
                    "model": model_output.model if model_output else "",
                    "input_tokens": model_output.input_tokens if model_output else 0,
                    "output_tokens": model_output.output_tokens if model_output else 0,
                    "estimated_cost": (
                        model_output.metadata.get("estimated_cost", "0.000000")
                        if model_output
                        else "0.000000"
                    ),
                    "currency": (
                        model_output.metadata.get("currency", "")
                        if model_output
                        else ""
                    ),
                    "notes": result.notes,
                }
            )
    return results


def write_benchmark_report(results: list[dict[str, Any]], path: Path | str) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps({"results": results}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return output_path


def _project_from_case(case: ReadingSampleBenchmarkCase) -> BookProject:
    return BookProject(
        name=case.book_name,
        interview=Interview(
            topic=case.topic,
            target_audience=case.target_audience,
            book_type=case.book_type,
            desired_result=case.chapter_goal,
            tone=case.tone,
            length_goal="Benchmark chapter",
            export_format="Markdown",
            value_proposition="Benchmark for chapter review quality.",
            reader_problem="Benchmark detects review quality issues.",
            book_category=case.book_category,
            age_group=case.age_group,
            narrative_focus=case.narrative_focus,
            perspective=case.perspective,
            perspective_count="eine Perspektive",
            ending_type="nicht relevant",
            publication_format="E-Book",
            character_mode="keine Figuren",
        ),
        project_id=f"benchmark-{case.case_id}",
    )


def _draft_from_case(case: ReadingSampleBenchmarkCase) -> ChapterDraft:
    return ChapterDraft(
        chapter_number=case.chapter_number,
        title=case.chapter_title,
        goal=case.chapter_goal,
        markdown=case.chapter_markdown,
        summary=case.chapter_goal,
        next_transition="Benchmark",
        open_points=[],
    )
