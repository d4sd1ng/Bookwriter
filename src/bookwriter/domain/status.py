from __future__ import annotations

from enum import StrEnum


class ApprovalStatus(StrEnum):
    DRAFT = "draft"
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    BLOCKED = "blocked"
    NEEDS_REVISION = "needs_revision"
    READY_FOR_WRITING = "ready_for_writing"
    READY_FOR_EDITING = "ready_for_editing"
    READY_FOR_EXPORT = "ready_for_export"
    EXPORTED = "exported"
    ARCHIVED = "archived"


class WorkflowStage(StrEnum):
    INTERVIEW = "interview"
    CONCEPT = "concept"
    OUTLINE = "outline"
    CHAPTER_BRIEFING = "chapter_briefing"
    DRAFTING = "drafting"
    EDITING = "editing"
    CONSISTENCY_REVIEW = "consistency_review"
    EXPORT_PREPARATION = "export_preparation"
    PUBLISHING_PREPARATION = "publishing_preparation"
