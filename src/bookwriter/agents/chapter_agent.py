from __future__ import annotations

import json
from pathlib import Path

from bookwriter.agents.base import AgentResult
from bookwriter.domain.models import (
    BookProject,
    ChapterBriefing,
    ChapterDraft,
    ChapterPlan,
    ChapterReview,
)
from bookwriter.domain.review_runs import READING_SAMPLE_SEQUENCE, ReadingSampleFocus
from bookwriter.domain.status import ApprovalStatus
from bookwriter.runtime.model_runtime import DisabledModelRuntime, ModelInvocation, ModelRuntime
from bookwriter.runtime.ollama_runtime import ModelRuntimeBlocked


class ChapterBriefingAgent:
    name = "Chapter Briefing Agent"

    def run(self, project: BookProject, chapter: ChapterPlan) -> AgentResult[ChapterBriefing]:
        briefing = ChapterBriefing(
            chapter_number=chapter.number,
            title=chapter.title,
            goal=chapter.goal,
            context=f"Chapter {chapter.number} in '{project.name}' for {project.interview.target_audience}.",
            core_points=chapter.core_points or ["chapter goal", "reader progress", "example"],
            section_structure=[
                "Opening: establish chapter question",
                "Main section: develop core points",
                "Application: example or scene",
                "Close: summarize and transition",
            ],
            examples=["Use an example that fits the target audience."],
            source_needs=["Mark claims that require approved sources."],
            previous_transition="Connect to the previous approved chapter if available.",
            next_transition="Prepare the reader for the next chapter.",
            status=ApprovalStatus.PENDING_REVIEW,
        )
        return AgentResult(
            agent=self.name,
            output=briefing,
            status=briefing.status,
            notes=["Chapter briefing created and waiting for approval."],
        )


class ChapterDraftAgent:
    name = "Chapter Draft Agent"

    def run(self, project: BookProject, briefing: ChapterBriefing) -> AgentResult[ChapterDraft]:
        markdown = (
            f"# {briefing.title}\n\n"
            f"## Ziel\n\n{briefing.goal}\n\n"
            "## Rohfassung\n\n"
            "Dieses Kapitel ist eine kontrollierte Rohfassung auf Basis des freigegebenen "
            "Kapitelbriefings. Es entwickelt die Kernpunkte, fuehrt ein passendes Beispiel "
            "ein und endet mit einem Uebergang.\n\n"
            "## Kernpunkte\n\n"
            + "\n".join(f"- {point}" for point in briefing.core_points)
            + "\n"
        )
        draft = ChapterDraft(
            chapter_number=briefing.chapter_number,
            title=briefing.title,
            goal=briefing.goal,
            markdown=markdown,
            summary=f"Rohfassung fuer Kapitel {briefing.chapter_number}: {briefing.goal}",
            next_transition=briefing.next_transition,
            open_points=["Needs five focused reading sample reviews before approval."],
            status=ApprovalStatus.PENDING_REVIEW,
        )
        return AgentResult(
            agent=self.name,
            output=draft,
            status=draft.status,
            notes=["Chapter draft created and waiting for review runs."],
        )


class ChapterReviewAgent:
    name = "Chapter Review Agent"

    def __init__(
        self,
        model_runtime: ModelRuntime | None = None,
        requested_model: str | None = None,
    ) -> None:
        self.model_runtime = model_runtime or DisabledModelRuntime()
        self.requested_model = requested_model
        self.last_model_output = None

    def run(
        self,
        project: BookProject,
        draft: ChapterDraft,
        focus: ReadingSampleFocus,
    ) -> AgentResult[ChapterReview]:
        run_number = READING_SAMPLE_SEQUENCE.index(focus) + 1
        if self.model_runtime.enabled:
            return self._run_model_backed(project, draft, focus, run_number)
        review = ChapterReview(
            chapter_number=draft.chapter_number,
            focus=focus.value,
            run_number=run_number,
            findings=[f"Review focus '{focus.value}' completed for chapter {draft.chapter_number}."],
            change_suggestions=["No automated final approval; review requires approval decision."],
            residual_risks=["This placeholder review must be replaced by model-backed review output."],
            status=ApprovalStatus.PENDING_REVIEW,
        )
        return AgentResult(
            agent=self.name,
            output=review,
            status=review.status,
            notes=[f"Chapter review run {run_number} created for focus {focus.value}."],
        )

    def _run_model_backed(
        self,
        project: BookProject,
        draft: ChapterDraft,
        focus: ReadingSampleFocus,
        run_number: int,
    ) -> AgentResult[ChapterReview]:
        try:
            output = self.model_runtime.invoke(
                ModelInvocation(
                    task="reading_sample_review",
                    prompt=_review_prompt(project, draft, focus, run_number),
                    project_id=project.project_id,
                    agent="text_analysis",
                    chapter_number=draft.chapter_number,
                    run_focus=focus.value,
                    model=self.requested_model,
                    expected_json=True,
                )
            )
            self.last_model_output = output
        except ModelRuntimeBlocked as error:
            review = ChapterReview(
                chapter_number=draft.chapter_number,
                focus=focus.value,
                run_number=run_number,
                findings=[],
                change_suggestions=[],
                residual_risks=error.blockers,
                status=ApprovalStatus.BLOCKED,
            )
            return AgentResult(
                agent=self.name,
                output=review,
                status=review.status,
                notes=["Model-backed review blocked by model routing rules."],
            )
        try:
            payload = _load_json_object(output.text)
        except ValueError:
            review = ChapterReview(
                chapter_number=draft.chapter_number,
                focus=focus.value,
                run_number=run_number,
                findings=[],
                change_suggestions=[],
                residual_risks=["Model response was not valid JSON for reading_sample_review."],
                status=ApprovalStatus.BLOCKED,
            )
            return AgentResult(
                agent=self.name,
                output=review,
                status=review.status,
                notes=["Model-backed review blocked because structured output was invalid."],
            )
        blockers = _as_string_list(payload.get("blocker", payload.get("blockers", [])))
        problems = payload.get("erkannte_probleme", [])
        findings = [_problem_to_finding(item) for item in problems] or [
            str(item) for item in payload.get("findings", [])
        ]
        review = ChapterReview(
            chapter_number=int(payload.get("kapitelnummer") or draft.chapter_number),
            focus=str(payload.get("fokus") or focus.value),
            run_number=int(payload.get("run_nummer") or run_number),
            findings=findings,
            change_suggestions=[
                str(item)
                for item in _as_string_list(payload.get(
                    "aenderungsvorschlaege",
                    payload.get("change_suggestions", []),
                ))
            ],
            residual_risks=[
                str(item)
                for item in _as_string_list(payload.get(
                    "restrisiken",
                    payload.get("residual_risks", blockers),
                ))
            ],
            status=ApprovalStatus.BLOCKED if blockers else ApprovalStatus.PENDING_REVIEW,
        )
        return AgentResult(
            agent=self.name,
            output=review,
            status=review.status,
            notes=[
                f"Model-backed chapter review run {run_number} created with {output.model}.",
                f"Tokens logged: {output.input_tokens + output.output_tokens}.",
            ],
        )


def _review_prompt(
    project: BookProject,
    draft: ChapterDraft,
    focus: ReadingSampleFocus,
    run_number: int,
) -> str:
    template = Path("prompts/reading_sample_review_prompt.md").read_text(encoding="utf-8")
    interview = project.interview
    previous_reviews = [
        {
            "focus": review.focus,
            "status": review.status.value,
        }
        for review in project.chapter_reviews
        if review.chapter_number == draft.chapter_number
    ]
    payload = {
        "auftrag_id": f"{project.project_id}-{draft.chapter_number}-{focus.value}",
        "kapitelnummer": draft.chapter_number,
        "kapiteltitel": draft.title,
        "kapitelziel": draft.goal,
        "fokus": focus.value,
        "run_nummer": run_number,
        "buchtyp": interview.book_type,
        "buchkategorie": interview.book_category,
        "zielgruppe": interview.target_audience,
        "altersgruppe": interview.age_group,
        "perspektive": interview.perspective,
        "erzaehlfokus": interview.narrative_focus,
        "stilvorgaben": interview.tone,
        "vorherige_leseproben": previous_reviews,
        "kapitelrohfassung_markdown": draft.markdown,
    }
    return template + "\n\n## Konkreter Auftrag\n\n" + json.dumps(
        payload,
        ensure_ascii=False,
        indent=2,
    )


def _load_json_object(text: str) -> dict[str, object]:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = stripped.strip("`")
        stripped = stripped.removeprefix("json").strip()
    payload = json.loads(stripped)
    if not isinstance(payload, dict):
        raise ValueError("Structured model output must be a JSON object.")
    return payload


def _problem_to_finding(problem: object) -> str:
    if not isinstance(problem, dict):
        return str(problem)
    location = str(problem.get("stelle", "")).strip()
    description = str(problem.get("problem", "")).strip()
    correction = str(problem.get("korrektur", "")).strip()
    priority = str(problem.get("prioritaet", "")).strip()
    parts = [part for part in [location, description, correction, priority] if part]
    return " | ".join(parts)


def _as_string_list(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    if isinstance(value, str):
        return [value] if value.strip() else []
    return [str(value)]
