from __future__ import annotations

from bookwriter.agents.base import AgentResult
from bookwriter.domain.models import MarketAssessment, BookProject
from bookwriter.domain.status import ApprovalStatus


class MarketAssessmentAgent:
    name = "Market Assessment Agent"

    def run(self, project: BookProject) -> AgentResult[MarketAssessment]:
        interview = project.interview
        assessment = MarketAssessment(
            positioning=(
                f"{interview.book_type.strip()} positioned for "
                f"{interview.target_audience.strip()} with a clear result promise."
            ),
            sales_chances=(
                "Preliminary: medium. A reliable rating requires category research, "
                "comparable titles, price bands, and audience access."
            ),
            strengths=[
                "Specific target audience is available.",
                "Reader outcome is explicit.",
                "Structured workflow can reduce quality variance.",
            ],
            risks=[
                "No approved source list yet.",
                "No competitive title analysis yet.",
                "No distribution channel decision approved yet.",
            ],
            next_checks=[
                "Approve target reader segment.",
                "Collect comparable books and current category data.",
                "Define price, format, and launch channel assumptions.",
            ],
            status=ApprovalStatus.PENDING_REVIEW,
        )
        return AgentResult(
            agent=self.name,
            output=assessment,
            status=assessment.status,
            notes=["Sales chance rating is preliminary until market data is approved."],
        )
