from __future__ import annotations

from dataclasses import dataclass

from bookwriter.domain.models import BookProject
from bookwriter.domain.status import ApprovalStatus, WorkflowStage


@dataclass(frozen=True, slots=True)
class ValidationResult:
    ok: bool
    blockers: list[str]


def validate_interview(project: BookProject) -> ValidationResult:
    interview = project.interview
    blockers: list[str] = []
    required_fields = {
        "topic": interview.topic,
        "target_audience": interview.target_audience,
        "book_type": interview.book_type,
        "desired_result": interview.desired_result,
        "tone": interview.tone,
        "length_goal": interview.length_goal,
        "export_format": interview.export_format,
        "reader_problem": interview.reader_problem,
        "value_proposition": interview.value_proposition,
    }
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


def validate_concept(project: BookProject) -> ValidationResult:
    blockers = validate_interview(project).blockers
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
    if not project.outline:
        blockers.append("No outline exists.")
    for chapter in project.outline:
        if not chapter.goal.strip():
            blockers.append(f"Contract rule: chapter {chapter.number} has no chapter goal.")
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
