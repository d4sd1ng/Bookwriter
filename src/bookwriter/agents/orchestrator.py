from __future__ import annotations

from bookwriter.agents.concept_agent import BookConceptAgent
from bookwriter.agents.brainstorm_agent import BrainstormAgent
from bookwriter.agents.market_agent import MarketAssessmentAgent
from bookwriter.agents.outline_agent import OutlineAgent
from bookwriter.agents.publisher_agent import PublisherOfferAgent
from bookwriter.domain.models import BookProject, Interview
from bookwriter.domain.status import ApprovalStatus, WorkflowStage
from bookwriter.domain.validation import (
    apply_blockers,
    validate_concept,
    validate_development_foundation,
    validate_interview,
)
from bookwriter.publishing.kdp import KdpPreparationService


class Orchestrator:
    def __init__(self) -> None:
        self.concept_agent = BookConceptAgent()
        self.brainstorm_agent = BrainstormAgent()
        self.outline_agent = OutlineAgent()
        self.market_agent = MarketAssessmentAgent()
        self.publisher_agent = PublisherOfferAgent()
        self.kdp_service = KdpPreparationService()

    def create_project(self, name: str, interview: Interview) -> BookProject:
        project = BookProject(name=name.strip() or interview.topic.strip(), interview=interview)
        validation = validate_interview(project)
        if not validation.ok:
            apply_blockers(project, validation)
            return project
        result = self.concept_agent.run(project)
        project.concept = result.output
        project.stage = WorkflowStage.CONCEPT
        project.status = result.status
        project.touch()
        return project

    def prepare_brainstorming(self, project: BookProject, seed: str = "") -> BookProject:
        result = self.brainstorm_agent.create_funnel(seed or project.interview.topic)
        project.brainstorming = result.output
        project.status = result.status
        project.touch()
        return project

    def approve_concept(self, project: BookProject, chapter_count: int | None = None) -> BookProject:
        validation = validate_interview(project)
        foundation_validation = validate_development_foundation(project)
        validation.blockers.extend(foundation_validation.blockers)
        validation = type(validation)(ok=not validation.blockers, blockers=validation.blockers)
        if not validation.ok:
            apply_blockers(project, validation)
            return project
        if project.concept is None:
            project.blockers = ["No concept available to approve."]
            project.status = ApprovalStatus.BLOCKED
            project.touch()
            return project
        project.concept.status = ApprovalStatus.APPROVED
        result = self.outline_agent.run(project, chapter_count=chapter_count)
        project.outline = result.output
        project.stage = WorkflowStage.OUTLINE
        project.status = result.status
        project.blockers = []
        project.touch()
        return project

    def prepare_market_assessment(self, project: BookProject) -> BookProject:
        validation = validate_concept(project)
        if not validation.ok:
            apply_blockers(project, validation)
            return project
        result = self.market_agent.run(project)
        project.market_assessment = result.output
        project.touch()
        return project

    def prepare_publisher_offer(self, project: BookProject, target_publisher: str) -> BookProject:
        validation = validate_concept(project)
        if not validation.ok:
            apply_blockers(project, validation)
            return project
        result = self.publisher_agent.run(project, target_publisher)
        project.publisher_offers.append(result.output)
        project.touch()
        return project

    def prepare_kdp_checklist(self, project: BookProject) -> BookProject:
        checklist = self.kdp_service.prepare_checklist(project)
        project.publishing_checklists.append(checklist)
        if checklist.blockers:
            project.blockers = checklist.blockers
            project.status = ApprovalStatus.BLOCKED
        project.stage = WorkflowStage.PUBLISHING_PREPARATION
        project.touch()
        return project
