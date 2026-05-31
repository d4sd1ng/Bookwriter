from __future__ import annotations

from bookwriter.agents.concept_agent import BookConceptAgent
from bookwriter.agents.brainstorm_agent import BrainstormAgent
from bookwriter.agents.chapter_agent import ChapterBriefingAgent, ChapterDraftAgent, ChapterReviewAgent
from bookwriter.agents.market_agent import MarketAssessmentAgent
from bookwriter.agents.outline_agent import OutlineAgent
from bookwriter.agents.plot_agent import PlotAgent, TreatmentAgent
from bookwriter.agents.publisher_agent import PublisherOfferAgent
from bookwriter.domain.models import BookProject, Interview
from bookwriter.domain.review_runs import ReadingSampleFocus
from bookwriter.domain.status import ApprovalStatus, WorkflowStage
from bookwriter.domain.validation import (
    apply_blockers,
    validate_concept,
    validate_chapter_approval,
    validate_chapter_briefing_readiness,
    validate_chapter_draft_readiness,
    validate_chapter_review_readiness,
    validate_development_foundation,
    validate_interview,
    validate_plotting_readiness,
    validate_treatment_readiness,
)
from bookwriter.publishing.kdp import KdpPreparationService
from bookwriter.runtime.model_runtime import ModelRuntime


class Orchestrator:
    def __init__(
        self,
        model_runtime: ModelRuntime | None = None,
        review_model: str | None = None,
    ) -> None:
        self.concept_agent = BookConceptAgent()
        self.brainstorm_agent = BrainstormAgent()
        self.chapter_briefing_agent = ChapterBriefingAgent()
        self.chapter_draft_agent = ChapterDraftAgent()
        self.chapter_review_agent = ChapterReviewAgent(
            model_runtime=model_runtime,
            requested_model=review_model,
        )
        self.outline_agent = OutlineAgent()
        self.plot_agent = PlotAgent()
        self.treatment_agent = TreatmentAgent()
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
        plotting_validation = validate_treatment_readiness(project)
        if not plotting_validation.ok:
            project.status = ApprovalStatus.APPROVED
            project.blockers = plotting_validation.blockers
            project.touch()
            return project
        result = self.outline_agent.run(project, chapter_count=chapter_count)
        project.outline = result.output
        project.stage = WorkflowStage.OUTLINE
        project.status = result.status
        project.blockers = []
        project.touch()
        return project

    def prepare_plot(self, project: BookProject) -> BookProject:
        validation = validate_plotting_readiness(project)
        if not validation.ok:
            apply_blockers(project, validation)
            return project
        result = self.plot_agent.run(project)
        project.plot = result.output
        project.status = result.status
        project.stage = WorkflowStage.CONCEPT
        project.blockers = []
        project.touch()
        return project

    def approve_plot(self, project: BookProject) -> BookProject:
        if project.plot is None:
            project.status = ApprovalStatus.BLOCKED
            project.blockers = ["No plot available to approve."]
            project.touch()
            return project
        project.plot.status = ApprovalStatus.APPROVED
        project.blockers = []
        project.touch()
        return project

    def prepare_treatment(self, project: BookProject) -> BookProject:
        validation = validate_treatment_readiness(project)
        if not validation.ok:
            apply_blockers(project, validation)
            return project
        result = self.treatment_agent.run(project)
        project.treatment = result.output
        project.status = result.status
        project.blockers = []
        project.touch()
        return project

    def approve_treatment_and_create_outline(
        self,
        project: BookProject,
        chapter_count: int | None = None,
    ) -> BookProject:
        if project.treatment is None:
            project.status = ApprovalStatus.BLOCKED
            project.blockers = ["No treatment available to approve."]
            project.touch()
            return project
        project.treatment.status = ApprovalStatus.APPROVED
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

    def prepare_chapter_briefing(self, project: BookProject, chapter_number: int) -> BookProject:
        validation = validate_chapter_briefing_readiness(project, chapter_number)
        if not validation.ok:
            apply_blockers(project, validation)
            return project
        chapter = next(item for item in project.outline if item.number == chapter_number)
        result = self.chapter_briefing_agent.run(project, chapter)
        project.chapter_briefings = [
            item for item in project.chapter_briefings if item.chapter_number != chapter_number
        ]
        project.chapter_briefings.append(result.output)
        project.status = result.status
        project.blockers = []
        project.touch()
        return project

    def approve_chapter_briefing(self, project: BookProject, chapter_number: int) -> BookProject:
        briefing = self._find_briefing(project, chapter_number)
        if briefing is None:
            project.status = ApprovalStatus.BLOCKED
            project.blockers = [f"Chapter briefing not found: {chapter_number}."]
        else:
            briefing.status = ApprovalStatus.APPROVED
            project.blockers = []
        project.touch()
        return project

    def draft_chapter(self, project: BookProject, chapter_number: int) -> BookProject:
        briefing = self._find_briefing(project, chapter_number)
        validation = validate_chapter_draft_readiness(briefing)
        if not validation.ok:
            apply_blockers(project, validation)
            return project
        result = self.chapter_draft_agent.run(project, briefing)
        project.chapter_drafts = [
            item for item in project.chapter_drafts if item.chapter_number != chapter_number
        ]
        project.chapter_drafts.append(result.output)
        project.status = result.status
        project.blockers = []
        project.touch()
        return project

    def review_chapter(
        self,
        project: BookProject,
        chapter_number: int,
        focus: ReadingSampleFocus,
    ) -> BookProject:
        draft = self._find_draft(project, chapter_number)
        validation = validate_chapter_review_readiness(draft)
        if not validation.ok:
            apply_blockers(project, validation)
            return project
        result = self.chapter_review_agent.run(project, draft, focus)
        project.chapter_reviews = [
            item
            for item in project.chapter_reviews
            if not (item.chapter_number == chapter_number and item.focus == focus.value)
        ]
        project.chapter_reviews.append(result.output)
        project.status = result.status
        project.blockers = result.output.residual_risks if result.status == ApprovalStatus.BLOCKED else []
        project.touch()
        return project

    def approve_chapter_review(
        self,
        project: BookProject,
        chapter_number: int,
        focus: ReadingSampleFocus,
    ) -> BookProject:
        review = next(
            (
                item
                for item in project.chapter_reviews
                if item.chapter_number == chapter_number and item.focus == focus.value
            ),
            None,
        )
        if review is None:
            project.status = ApprovalStatus.BLOCKED
            project.blockers = [f"Chapter review not found: {chapter_number} / {focus.value}."]
        else:
            review.status = ApprovalStatus.APPROVED
            project.blockers = []
        project.touch()
        return project

    def approve_chapter(self, project: BookProject, chapter_number: int) -> BookProject:
        validation = validate_chapter_approval(project, chapter_number)
        if not validation.ok:
            apply_blockers(project, validation)
            return project
        draft = self._find_draft(project, chapter_number)
        if draft:
            draft.status = ApprovalStatus.APPROVED
        chapter = next((item for item in project.outline if item.number == chapter_number), None)
        if chapter:
            chapter.status = ApprovalStatus.APPROVED
        project.status = ApprovalStatus.APPROVED
        project.blockers = []
        project.touch()
        return project

    @staticmethod
    def _find_briefing(project: BookProject, chapter_number: int):
        return next(
            (item for item in project.chapter_briefings if item.chapter_number == chapter_number),
            None,
        )

    @staticmethod
    def _find_draft(project: BookProject, chapter_number: int):
        return next(
            (item for item in project.chapter_drafts if item.chapter_number == chapter_number),
            None,
        )
