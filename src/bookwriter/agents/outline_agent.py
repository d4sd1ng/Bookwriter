from __future__ import annotations

import re

from bookwriter.agents.base import AgentResult
from bookwriter.domain.models import BookProject, ChapterPlan
from bookwriter.domain.status import ApprovalStatus


class OutlineAgent:
    name = "Outline Agent"

    def run(self, project: BookProject, chapter_count: int | None = None) -> AgentResult[list[ChapterPlan]]:
        if project.concept is None:
            raise ValueError("Outline requires an approved concept.")
        count = chapter_count or _infer_chapter_count(project.interview.length_goal)
        topic = project.interview.topic.strip()
        chapters = [
            ChapterPlan(
                number=1,
                title=f"Orientation: {topic}",
                goal="Clarify the reader problem, promise, and boundaries.",
                core_points=["reader problem", "desired result", "scope"],
            ),
            ChapterPlan(
                number=2,
                title="Foundations",
                goal="Build the concepts needed before practical work starts.",
                core_points=["terms", "principles", "decision criteria"],
            ),
        ]
        while len(chapters) < max(count - 1, 2):
            number = len(chapters) + 1
            chapters.append(
                ChapterPlan(
                    number=number,
                    title=f"Practice Step {number - 2}",
                    goal=f"Move the reader one step closer to {project.interview.desired_result}.",
                    core_points=["method", "example", "common mistakes"],
                )
            )
        chapters.append(
            ChapterPlan(
                number=len(chapters) + 1,
                title="Implementation and Next Steps",
                goal="Turn the book's content into a usable action plan.",
                core_points=["summary", "checklist", "next actions"],
            )
        )
        return AgentResult(
            agent=self.name,
            output=chapters,
            status=ApprovalStatus.PENDING_REVIEW,
            notes=["Outline created with mandatory chapter goals."],
        )


def _infer_chapter_count(length_goal: str) -> int:
    match = re.search(r"\d+", length_goal)
    if not match:
        return 8
    value = int(match.group())
    if value <= 12:
        return max(4, value)
    if value < 120:
        return 6
    if value < 220:
        return 8
    return 10
