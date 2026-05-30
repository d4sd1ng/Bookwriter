from __future__ import annotations

from bookwriter.agents.base import AgentResult
from bookwriter.domain.models import BookConcept, BookProject
from bookwriter.domain.status import ApprovalStatus


class BookConceptAgent:
    name = "Book Concept Agent"

    def run(self, project: BookProject) -> AgentResult[BookConcept]:
        interview = project.interview
        value_proposition = interview.value_proposition.strip()
        if not value_proposition:
            value_proposition = (
                f"Readers in '{interview.target_audience}' get a practical path to "
                f"{interview.desired_result}."
            )

        reader_problem = interview.reader_problem.strip()
        if not reader_problem:
            reader_problem = (
                f"The target audience needs orientation and a clear structure for "
                f"'{interview.topic}'."
            )

        concept = BookConcept(
            working_title=interview.topic.strip().title(),
            subtitle=f"A {interview.book_type.strip()} for {interview.target_audience.strip()}",
            target_audience=interview.target_audience.strip(),
            reader_problem=reader_problem,
            value_proposition=value_proposition,
            boundary="No YouTube, LinkedIn, shorts, social media, or video workflows.",
            tone=interview.tone.strip(),
            open_questions=[
                "Which sources are approved for claims?",
                "Which examples may be used?",
                "Who approves style and structure?",
            ],
            status=ApprovalStatus.PENDING_REVIEW,
        )
        return AgentResult(
            agent=self.name,
            output=concept,
            status=concept.status,
            notes=["Concept created and waiting for approval."],
        )
