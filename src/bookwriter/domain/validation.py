from __future__ import annotations

from dataclasses import dataclass

from bookwriter.domain.models import BookProject, ChapterBriefing, ChapterDraft
from bookwriter.domain.review_runs import READING_SAMPLE_SEQUENCE
from bookwriter.domain.status import ApprovalStatus, WorkflowStage


@dataclass(frozen=True, slots=True)
class ValidationResult:
    ok: bool
    blockers: list[str]


def validate_interview(project: BookProject) -> ValidationResult:
    interview = project.interview
    blockers: list[str] = []
    required_fields = {
        "target_audience": interview.target_audience,
        "book_type": interview.book_type,
        "desired_result": interview.desired_result,
        "tone": interview.tone,
        "length_goal": interview.length_goal,
        "export_format": interview.export_format,
        "reader_problem": interview.reader_problem,
        "value_proposition": interview.value_proposition,
    }
    if interview.start_mode != "brainstorming":
        required_fields["topic"] = interview.topic
    for field_name, value in required_fields.items():
        if not value.strip():
            blockers.append(f"Missing required interview input: {field_name}")
    if not interview.target_audience.strip():
        blockers.append("Contract rule: no book without target audience.")
    if not interview.reader_problem.strip():
        blockers.append("Contract rule: no book without reader problem.")
    if not interview.value_proposition.strip():
        blockers.append("Contract rule: no outline without value proposition.")
    return ValidationResult(ok=not blockers, blockers=blockers)


def validate_development_foundation(project: BookProject) -> ValidationResult:
    interview = project.interview
    blockers: list[str] = []
    required_fields = {
        "book_category": interview.book_category,
        "age_group": interview.age_group,
        "narrative_focus": interview.narrative_focus,
        "perspective": interview.perspective,
        "perspective_count": interview.perspective_count,
        "ending_type": interview.ending_type,
        "publication_format": interview.publication_format,
        "character_mode": interview.character_mode,
    }
    for field_name, value in required_fields.items():
        if not value.strip():
            blockers.append(f"Missing required development foundation input: {field_name}")
    if interview.start_mode == "brainstorming" and not interview.selected_idea.strip():
        blockers.append("Brainstorming mode requires one selected idea before plotting.")
    if interview.existing_text_status == "provided_unapproved":
        blockers.append("Existing text must be approved before use.")
    if interview.research_mode == "scraping" and not interview.research_sources_approved:
        blockers.append("Scraping requires approved sources before research can run.")
    return ValidationResult(ok=not blockers, blockers=blockers)


def validate_concept(project: BookProject) -> ValidationResult:
    blockers = validate_interview(project).blockers
    blockers.extend(validate_development_foundation(project).blockers)
    if project.concept is None:
        blockers.append("No book concept exists.")
    else:
        if not project.concept.value_proposition.strip():
            blockers.append("Contract rule: no outline without value proposition.")
        if project.concept.status != ApprovalStatus.APPROVED:
            blockers.append("Book concept is not approved.")
    return ValidationResult(ok=not blockers, blockers=blockers)


def validate_outline(project: BookProject) -> ValidationResult:
    blockers = validate_concept(project).blockers
    if project.plot is None:
        blockers.append("No approved plot exists.")
    elif project.plot.status != ApprovalStatus.APPROVED:
        blockers.append("Plot is not approved.")
    if project.treatment is None:
        blockers.append("No approved treatment exists.")
    elif project.treatment.status != ApprovalStatus.APPROVED:
        blockers.append("Treatment is not approved.")
    if not project.outline:
        blockers.append("No outline exists.")
    for chapter in project.outline:
        if not chapter.goal.strip():
            blockers.append(f"Contract rule: chapter {chapter.number} has no chapter goal.")
    return ValidationResult(ok=not blockers, blockers=blockers)


def validate_plotting_readiness(project: BookProject) -> ValidationResult:
    blockers = validate_concept(project).blockers
    if project.concept is None or project.concept.status != ApprovalStatus.APPROVED:
        blockers.append("Approved concept is required before plotting.")
    return ValidationResult(ok=not blockers, blockers=blockers)


def validate_treatment_readiness(project: BookProject) -> ValidationResult:
    blockers = validate_plotting_readiness(project).blockers
    if project.plot is None:
        blockers.append("Plot is required before treatment.")
    elif project.plot.status != ApprovalStatus.APPROVED:
        blockers.append("Plot must be approved before treatment.")
    return ValidationResult(ok=not blockers, blockers=blockers)


def validate_chapter_briefing_readiness(
    project: BookProject,
    chapter_number: int,
) -> ValidationResult:
    blockers = validate_concept(project).blockers
    if project.stage != WorkflowStage.OUTLINE:
        blockers.append("Project must be in outline stage before chapter briefing.")
    if not project.outline:
        blockers.append("Approved outline is required before chapter briefing.")
    chapter = next((item for item in project.outline if item.number == chapter_number), None)
    if chapter is None:
        blockers.append(f"Chapter {chapter_number} not found in outline.")
    elif not chapter.goal.strip():
        blockers.append(f"Chapter {chapter_number} has no chapter goal.")
    return ValidationResult(ok=not blockers, blockers=blockers)


def validate_chapter_draft_readiness(briefing: ChapterBriefing | None) -> ValidationResult:
    blockers: list[str] = []
    if briefing is None:
        blockers.append("Approved chapter briefing is required before drafting.")
    elif briefing.status != ApprovalStatus.APPROVED:
        blockers.append("Chapter briefing is not approved.")
    return ValidationResult(ok=not blockers, blockers=blockers)


def validate_chapter_review_readiness(draft: ChapterDraft | None) -> ValidationResult:
    blockers: list[str] = []
    if draft is None:
        blockers.append("Chapter draft is required before review.")
    elif draft.status != ApprovalStatus.PENDING_REVIEW:
        blockers.append("Chapter draft must be pending_review before review.")
    return ValidationResult(ok=not blockers, blockers=blockers)


def validate_chapter_approval(project: BookProject, chapter_number: int) -> ValidationResult:
    blockers: list[str] = []
    draft = next(
        (item for item in project.chapter_drafts if item.chapter_number == chapter_number),
        None,
    )
    if draft is None:
        blockers.append("Chapter draft is required before approval.")
    required = {focus.value for focus in READING_SAMPLE_SEQUENCE}
    completed = {
        review.focus
        for review in project.chapter_reviews
        if review.chapter_number == chapter_number and review.status == ApprovalStatus.APPROVED
    }
    missing = sorted(required - completed)
    if missing:
        blockers.append(f"Missing approved chapter review runs: {', '.join(missing)}.")
    return ValidationResult(ok=not blockers, blockers=blockers)


def validate_export_readiness(project: BookProject) -> ValidationResult:
    blockers = validate_outline(project).blockers
    if project.stage != WorkflowStage.EXPORT_PREPARATION:
        blockers.append("Project is not in export preparation stage.")
    if project.status != ApprovalStatus.READY_FOR_EXPORT:
        blockers.append("Project status is not ready_for_export.")
    return ValidationResult(ok=not blockers, blockers=blockers)


def apply_blockers(project: BookProject, validation: ValidationResult) -> None:
    project.blockers = validation.blockers
    project.status = ApprovalStatus.BLOCKED if validation.blockers else project.status
    project.touch()
