from __future__ import annotations

from bookwriter.agents.base import AgentResult
from bookwriter.domain.models import BookProject, PublisherOffer
from bookwriter.domain.status import ApprovalStatus


class PublisherOfferAgent:
    name = "Publisher Offer Agent"

    def run(self, project: BookProject, target_publisher: str) -> AgentResult[PublisherOffer]:
        if project.concept is None:
            raise ValueError("Publisher offer requires a concept.")
        publisher = target_publisher.strip() or "Target publisher"
        offer = PublisherOffer(
            target_publisher=publisher,
            pitch=(
                f"Proposal for '{project.concept.working_title}': "
                f"{project.concept.value_proposition}"
            ),
            selling_points=[
                f"Clear audience: {project.concept.target_audience}",
                f"Defined reader problem: {project.concept.reader_problem}",
                f"Format: {project.interview.book_type}",
            ],
            requested_materials=[
                "Approved concept",
                "Approved outline",
                "Author bio",
                "Sample chapter",
                "Comparable title analysis",
                "Market assessment",
            ],
            risks=[
                "Offer is not ready to send before concept, outline, and market assessment approval.",
                "Publisher-specific submission rules must be checked manually.",
            ],
            status=ApprovalStatus.PENDING_REVIEW,
        )
        return AgentResult(
            agent=self.name,
            output=offer,
            status=offer.status,
            notes=["Publisher offer prepared as draft material."],
        )
