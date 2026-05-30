from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from bookwriter.domain.status import ApprovalStatus, WorkflowStage


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


@dataclass(slots=True)
class Interview:
    topic: str
    target_audience: str
    book_type: str
    desired_result: str
    tone: str
    length_goal: str
    export_format: str
    value_proposition: str = ""
    reader_problem: str = ""
    sales_goal: str = ""


@dataclass(slots=True)
class ChapterPlan:
    number: int
    title: str
    goal: str
    core_points: list[str] = field(default_factory=list)
    status: ApprovalStatus = ApprovalStatus.DRAFT


@dataclass(slots=True)
class BookConcept:
    working_title: str
    subtitle: str
    target_audience: str
    reader_problem: str
    value_proposition: str
    boundary: str
    tone: str
    open_questions: list[str] = field(default_factory=list)
    status: ApprovalStatus = ApprovalStatus.PENDING_REVIEW


@dataclass(slots=True)
class MarketAssessment:
    positioning: str
    sales_chances: str
    strengths: list[str]
    risks: list[str]
    next_checks: list[str]
    status: ApprovalStatus = ApprovalStatus.PENDING_REVIEW


@dataclass(slots=True)
class PublisherOffer:
    target_publisher: str
    pitch: str
    selling_points: list[str]
    requested_materials: list[str]
    risks: list[str]
    status: ApprovalStatus = ApprovalStatus.PENDING_REVIEW


@dataclass(slots=True)
class PublishingChecklist:
    platform: str
    required_status: ApprovalStatus
    items: list[str]
    blockers: list[str]
    status: ApprovalStatus = ApprovalStatus.BLOCKED


@dataclass(slots=True)
class BookProject:
    name: str
    interview: Interview
    project_id: str = field(default_factory=lambda: uuid4().hex[:12])
    stage: WorkflowStage = WorkflowStage.INTERVIEW
    status: ApprovalStatus = ApprovalStatus.DRAFT
    concept: BookConcept | None = None
    outline: list[ChapterPlan] = field(default_factory=list)
    market_assessment: MarketAssessment | None = None
    publisher_offers: list[PublisherOffer] = field(default_factory=list)
    publishing_checklists: list[PublishingChecklist] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=utc_now_iso)
    updated_at: str = field(default_factory=utc_now_iso)

    def touch(self) -> None:
        self.updated_at = utc_now_iso()

    def to_dict(self) -> dict[str, Any]:
        return _to_plain(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> BookProject:
        interview = Interview(**data["interview"])
        concept_data = data.get("concept")
        if concept_data:
            concept_data["status"] = ApprovalStatus(concept_data["status"])
            concept = BookConcept(**concept_data)
        else:
            concept = None
        outline = [
            ChapterPlan(**(item | {"status": ApprovalStatus(item["status"])}))
            for item in data.get("outline", [])
        ]
        market_data = data.get("market_assessment")
        if market_data:
            market_data["status"] = ApprovalStatus(market_data["status"])
            market_assessment = MarketAssessment(**market_data)
        else:
            market_assessment = None
        publisher_offers = [
            PublisherOffer(**(item | {"status": ApprovalStatus(item["status"])}))
            for item in data.get("publisher_offers", [])
        ]
        publishing_checklists = [
            PublishingChecklist(
                **(
                    item
                    | {
                        "required_status": ApprovalStatus(item["required_status"]),
                        "status": ApprovalStatus(item["status"]),
                    }
                )
            )
            for item in data.get("publishing_checklists", [])
        ]
        return cls(
            project_id=data["project_id"],
            name=data["name"],
            interview=interview,
            stage=WorkflowStage(data.get("stage", WorkflowStage.INTERVIEW)),
            status=ApprovalStatus(data.get("status", ApprovalStatus.DRAFT)),
            concept=concept,
            outline=outline,
            market_assessment=market_assessment,
            publisher_offers=publisher_offers,
            publishing_checklists=publishing_checklists,
            blockers=list(data.get("blockers", [])),
            created_at=data.get("created_at", utc_now_iso()),
            updated_at=data.get("updated_at", utc_now_iso()),
        )


def _to_plain(value: Any) -> Any:
    if isinstance(value, ApprovalStatus | WorkflowStage):
        return value.value
    if hasattr(value, "__dataclass_fields__"):
        return {
            key: _to_plain(getattr(value, key))
            for key in value.__dataclass_fields__
        }
    if isinstance(value, list):
        return [_to_plain(item) for item in value]
    if isinstance(value, dict):
        return {key: _to_plain(item) for key, item in value.items()}
    return value
