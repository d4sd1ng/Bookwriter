from __future__ import annotations

from bookwriter.agents.orchestrator import Orchestrator
from bookwriter.domain.models import Interview
from bookwriter.domain.status import ApprovalStatus, WorkflowStage
from bookwriter.storage.json_store import JsonProjectStore


def interview(**overrides: str) -> Interview:
    data = {
        "topic": "AI for consultants",
        "target_audience": "Independent consultants",
        "book_type": "Practical guide",
        "desired_result": "build a repeatable AI advisory offer",
        "tone": "direct and practical",
        "length_goal": "8 chapters",
        "export_format": "Markdown",
        "value_proposition": "A clear offer-building path for consultants.",
        "reader_problem": "They know AI matters but cannot package it.",
        "sales_goal": "Validate ebook potential.",
    }
    data.update(overrides)
    return Interview(**data)


def test_missing_target_audience_blocks_project() -> None:
    project = Orchestrator().create_project("Blocked", interview(target_audience=""))

    assert project.status == ApprovalStatus.BLOCKED
    assert any("target audience" in blocker for blocker in project.blockers)
    assert project.concept is None


def test_concept_approval_creates_outline_with_goals() -> None:
    orchestrator = Orchestrator()
    project = orchestrator.create_project("Guide", interview())

    updated = orchestrator.approve_concept(project, chapter_count=5)

    assert updated.stage == WorkflowStage.OUTLINE
    assert updated.status == ApprovalStatus.PENDING_REVIEW
    assert len(updated.outline) == 5
    assert all(chapter.goal for chapter in updated.outline)


def test_market_and_publisher_prepare_after_concept_approval() -> None:
    orchestrator = Orchestrator()
    project = orchestrator.create_project("Guide", interview())
    project = orchestrator.approve_concept(project)

    project = orchestrator.prepare_market_assessment(project)
    project = orchestrator.prepare_publisher_offer(project, "Example Verlag")

    assert project.market_assessment is not None
    assert project.publisher_offers[-1].target_publisher == "Example Verlag"


def test_kdp_checklist_blocks_until_export_ready() -> None:
    orchestrator = Orchestrator()
    project = orchestrator.create_project("Guide", interview())
    project = orchestrator.approve_concept(project)

    updated = orchestrator.prepare_kdp_checklist(project)

    assert updated.publishing_checklists[-1].platform == "Amazon KDP"
    assert updated.publishing_checklists[-1].status == ApprovalStatus.BLOCKED
    assert updated.blockers


def test_json_store_roundtrip(tmp_path) -> None:
    store = JsonProjectStore(tmp_path)
    project = Orchestrator().create_project("Guide", interview())
    store.save(project)

    loaded = store.load(project.project_id)

    assert loaded.project_id == project.project_id
    assert loaded.concept is not None
    assert loaded.concept.status == ApprovalStatus.PENDING_REVIEW
