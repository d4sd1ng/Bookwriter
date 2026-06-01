from __future__ import annotations

from bookwriter.agents.orchestrator import Orchestrator
from bookwriter.domain.models import Interview
from bookwriter.domain.review_runs import READING_SAMPLE_SEQUENCE
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
        "book_category": "Sachbuch",
        "age_group": "Erwachsene",
        "narrative_focus": "handlungsorientiert",
        "perspective": "3. Person",
        "perspective_count": "eine Perspektive",
        "ending_type": "offenes Ende",
        "publication_format": "E-Book",
        "character_mode": "keine Figuren",
    }
    data.update(overrides)
    return Interview(**data)


def test_missing_target_audience_blocks_project() -> None:
    project = Orchestrator().create_project("Blocked", interview(target_audience=""))

    assert project.status == ApprovalStatus.BLOCKED
    assert any("target audience" in blocker for blocker in project.blockers)
    assert project.concept is None


def test_concept_approval_requires_plot_and_treatment_before_outline() -> None:
    orchestrator = Orchestrator()
    project = orchestrator.create_project("Guide", interview())

    updated = orchestrator.approve_concept(project, chapter_count=5)

    assert updated.status == ApprovalStatus.APPROVED
    assert not updated.outline
    assert any("Plot" in blocker or "Treatment" in blocker for blocker in updated.blockers)


def test_plot_treatment_approval_creates_outline_with_goals() -> None:
    orchestrator = Orchestrator()
    project = orchestrator.create_project("Guide", interview())
    project = orchestrator.approve_concept(project)
    project.blockers = []
    project = orchestrator.prepare_plot(project)
    project = orchestrator.approve_plot(project)
    project = orchestrator.prepare_treatment(project)

    updated = orchestrator.approve_treatment_and_create_outline(project, chapter_count=5)

    assert updated.stage == WorkflowStage.OUTLINE
    assert updated.status == ApprovalStatus.PENDING_REVIEW
    assert len(updated.outline) == 5
    assert all(chapter.goal for chapter in updated.outline)


def test_concept_approval_blocks_without_development_foundation() -> None:
    orchestrator = Orchestrator()
    project = orchestrator.create_project("Guide", interview(book_category=""))

    updated = orchestrator.approve_concept(project, chapter_count=5)

    assert updated.status == ApprovalStatus.BLOCKED
    assert any("book_category" in blocker for blocker in updated.blockers)


def test_market_and_publisher_prepare_after_concept_approval() -> None:
    orchestrator = Orchestrator()
    project = orchestrator.create_project("Guide", interview())
    project = orchestrator.approve_concept(project)
    project.blockers = []
    project = orchestrator.prepare_plot(project)
    project = orchestrator.approve_plot(project)
    project = orchestrator.prepare_treatment(project)
    project = orchestrator.approve_treatment_and_create_outline(project)

    project = orchestrator.prepare_market_assessment(project)
    project = orchestrator.prepare_publisher_offer(project, "Example Verlag")

    assert project.market_assessment is not None
    assert project.publisher_offers[-1].target_publisher == "Example Verlag"


def test_kdp_checklist_blocks_until_export_ready() -> None:
    orchestrator = Orchestrator()
    project = orchestrator.create_project("Guide", interview())
    project = orchestrator.approve_concept(project)
    project.blockers = []
    project = orchestrator.prepare_plot(project)
    project = orchestrator.approve_plot(project)
    project = orchestrator.prepare_treatment(project)
    project = orchestrator.approve_treatment_and_create_outline(project)

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


def test_brainstorming_funnel_creates_5_3_1_options() -> None:
    project = Orchestrator().create_project("Guide", interview(start_mode="brainstorming"))

    updated = Orchestrator().prepare_brainstorming(project, seed="Mut")

    assert updated.brainstorming is not None
    assert len(updated.brainstorming.proposals_5) == 5
    assert len(updated.brainstorming.proposals_3) == 3
    assert updated.brainstorming.selected_1 is not None


def test_chapter_pipeline_blocks_approval_until_all_reviews_are_approved() -> None:
    orchestrator = Orchestrator()
    project = _outlined_project(orchestrator)
    project = orchestrator.prepare_chapter_briefing(project, 1)
    project = orchestrator.approve_chapter_briefing(project, 1)
    project = orchestrator.draft_chapter(project, 1)
    project = orchestrator.review_chapter(project, 1, READING_SAMPLE_SEQUENCE[0])
    project = orchestrator.approve_chapter_review(project, 1, READING_SAMPLE_SEQUENCE[0])

    updated = orchestrator.approve_chapter(project, 1)

    assert updated.status == ApprovalStatus.BLOCKED
    assert any("Missing approved chapter review runs" in blocker for blocker in updated.blockers)


def test_chapter_pipeline_approves_after_five_reviews() -> None:
    orchestrator = Orchestrator()
    project = _outlined_project(orchestrator)
    project = orchestrator.prepare_chapter_briefing(project, 1)
    project = orchestrator.approve_chapter_briefing(project, 1)
    project = orchestrator.draft_chapter(project, 1)
    for focus in READING_SAMPLE_SEQUENCE:
        project = orchestrator.review_chapter(project, 1, focus)
        project = orchestrator.approve_chapter_review(project, 1, focus)

    updated = orchestrator.approve_chapter(project, 1)

    assert updated.status == ApprovalStatus.APPROVED
    assert updated.chapter_drafts[0].status == ApprovalStatus.APPROVED
    assert updated.outline[0].status == ApprovalStatus.APPROVED


def test_chapter_revision_blocks_until_all_reviews_are_approved() -> None:
    orchestrator = Orchestrator()
    project = _outlined_project(orchestrator)
    project = orchestrator.prepare_chapter_briefing(project, 1)
    project = orchestrator.approve_chapter_briefing(project, 1)
    project = orchestrator.draft_chapter(project, 1)
    project = orchestrator.review_chapter(project, 1, READING_SAMPLE_SEQUENCE[0])
    project = orchestrator.approve_chapter_review(project, 1, READING_SAMPLE_SEQUENCE[0])

    updated = orchestrator.revise_chapter(project, 1)

    assert updated.status == ApprovalStatus.BLOCKED
    assert any("Missing approved chapter review runs before revision" in blocker for blocker in updated.blockers)


def test_chapter_revision_creates_revised_draft_after_five_reviews() -> None:
    orchestrator = Orchestrator()
    project = _outlined_project(orchestrator)
    project = orchestrator.prepare_chapter_briefing(project, 1)
    project = orchestrator.approve_chapter_briefing(project, 1)
    project = orchestrator.draft_chapter(project, 1)
    for focus in READING_SAMPLE_SEQUENCE:
        project = orchestrator.review_chapter(project, 1, focus)
        project = orchestrator.approve_chapter_review(project, 1, focus)

    updated = orchestrator.revise_chapter(project, 1)

    assert updated.status == ApprovalStatus.PENDING_REVIEW
    assert "## Ueberarbeitungshinweise" in updated.chapter_drafts[0].markdown


def _outlined_project(orchestrator: Orchestrator):
    project = orchestrator.create_project("Guide", interview())
    project = orchestrator.approve_concept(project)
    project.blockers = []
    project = orchestrator.prepare_plot(project)
    project = orchestrator.approve_plot(project)
    project = orchestrator.prepare_treatment(project)
    return orchestrator.approve_treatment_and_create_outline(project, chapter_count=3)
