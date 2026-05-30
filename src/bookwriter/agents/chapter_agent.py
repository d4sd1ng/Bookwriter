from __future__ import annotations

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

    def run(self, draft: ChapterDraft, focus: ReadingSampleFocus) -> AgentResult[ChapterReview]:
        run_number = READING_SAMPLE_SEQUENCE.index(focus) + 1
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
