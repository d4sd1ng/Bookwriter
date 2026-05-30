from __future__ import annotations

from bookwriter.domain.models import BookProject, PublishingChecklist
from bookwriter.domain.status import ApprovalStatus
from bookwriter.domain.validation import validate_export_readiness


class KdpPreparationService:
    platform = "Amazon KDP"

    def prepare_checklist(self, project: BookProject) -> PublishingChecklist:
        validation = validate_export_readiness(project)
        status = ApprovalStatus.PENDING_REVIEW if validation.ok else ApprovalStatus.BLOCKED
        return PublishingChecklist(
            platform=self.platform,
            required_status=ApprovalStatus.READY_FOR_EXPORT,
            items=[
                "Approved final manuscript",
                "Approved title and subtitle",
                "Approved description and keywords",
                "Approved categories",
                "Cover file",
                "Interior file",
                "ISBN decision",
                "Price and royalty decision",
                "Territories and rights confirmation",
                "Final manual upload approval",
            ],
            blockers=validation.blockers,
            status=status,
        )
