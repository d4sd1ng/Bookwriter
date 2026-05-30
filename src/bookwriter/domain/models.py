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
    start_mode: str = "idea"
    existing_text_status: str = "none"
    selected_idea: str = ""
    book_category: str = ""
    age_group: str = ""
    narrative_focus: str = ""
    perspective: str = ""
    perspective_count: str = ""
    ending_type: str = ""
    publication_format: str = ""
    character_mode: str = ""
    character_brief: str = ""
    research_mode: str = "none"
    research_sources_approved: bool = False
    manual_approval_after_each_review: bool = True


@dataclass(slots=True)
class IdeaProposal:
    title: str
    category: str
    target_audience: str
    premise: str
    what_if: str
    conflict: str
    format_hint: str


@dataclass(slots=True)
class BrainstormingFunnel:
    seed: str
    proposals_5: list[IdeaProposal] = field(default_factory=list)
    proposals_3: list[IdeaProposal] = field(default_factory=list)
    selected_1: IdeaProposal | None = None
    status: ApprovalStatus = ApprovalStatus.DRAFT


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
    brainstorming: BrainstormingFunnel | None = None
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
        brainstorming_data = data.get("brainstorming")
        if brainstorming_data:
            brainstorming_data["status"] = ApprovalStatus(brainstorming_data["status"])
            if brainstorming_data.get("selected_1"):
                brainstorming_data["selected_1"] = IdeaProposal(**brainstorming_data["selected_1"])
            brainstorming_data["proposals_5"] = [
                IdeaProposal(**item) for item in brainstorming_data.get("proposals_5", [])
            ]
            brainstorming_data["proposals_3"] = [
                IdeaProposal(**item) for item in brainstorming_data.get("proposals_3", [])
            ]
            brainstorming = BrainstormingFunnel(**brainstorming_data)
        else:
            brainstorming = None
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
            brainstorming=brainstorming,
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
