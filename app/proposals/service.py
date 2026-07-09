from uuid import UUID

from fastapi import HTTPException

from app.groups.repository import GroupRepository
from app.models.proposal import Proposal
from app.notifications.service import NotificationService
from app.proposals.repository import ProposalRepository


class ProposalService:

    def __init__(self, db):
        self.db = db
        self.repo = ProposalRepository(db)
        self.group_repo = GroupRepository(db)
        self.notification = NotificationService(db)

    # =====================================================
    # CREATE
    # =====================================================

    async def create_proposal(
        self,
        current_user,
        group_id: UUID,
        data,
    ):
        student = await self.group_repo.get_student(
            current_user.id
        )

        if not student:
            raise HTTPException(
                status_code=403,
                detail="Only students can submit proposals.",
            )

        membership = await self.group_repo.get_group_membership(
            student.id
        )

        if not membership:
            raise HTTPException(
                status_code=403,
                detail="You are not a member of any group.",
            )

        if membership.group_id != group_id:
            raise HTTPException(
                status_code=403,
                detail="You are not a member of this group.",
            )

        group = await self.repo.get_group(group_id)

        if not group:
            raise HTTPException(
                status_code=404,
                detail="Group not found.",
            )

        existing = await self.repo.get_group_proposal(
            group_id
        )

        if existing:
            raise HTTPException(
                status_code=400,
                detail="This group already has a proposal.",
            )

        proposal = Proposal(
            group_id=group_id,
            professor_id=data.professor_id,
            title=data.title,
            abstract=data.abstract,
            objectives=data.objectives,
            status="Pending",
        )

        await self.repo.create_proposal(
            proposal
        )

        await self.db.commit()

        professor = await self.repo.get_professor_by_id(
            data.professor_id
        )

        if professor:
            await self.notification.create(
                user_id=professor.user_id,
                title="New Proposal Submitted",
                message=f"A new proposal '{proposal.title}' requires your review.",
                type="Proposal",
            )

        return proposal

    # =====================================================
    # PENDING
    # =====================================================

    async def get_pending_proposals(
        self,
        current_user,
    ):
        professor = await self.repo.get_professor(
            current_user.id
        )

        if not professor:
            raise HTTPException(
                status_code=403,
                detail="Only professors can review proposals.",
            )

        return await self.repo.get_pending_proposals(
            professor.id
        )

    # =====================================================
    # APPROVE
    # =====================================================

    async def approve_proposal(
        self,
        current_user,
        proposal_id: UUID,
    ):
        professor = await self.repo.get_professor(
            current_user.id
        )

        if not professor:
            raise HTTPException(
                status_code=403,
                detail="Only professors can approve proposals.",
            )

        proposal = await self.repo.get_proposal(
            proposal_id
        )

        if not proposal:
            raise HTTPException(
                status_code=404,
                detail="Proposal not found.",
            )

        if proposal.professor_id != professor.id:
            raise HTTPException(
                status_code=403,
                detail="This proposal is not assigned to you.",
            )

        proposal.status = "Approved"

        await self.repo.update_proposal(
            proposal
        )

        await self.db.commit()

        for member in proposal.group.members:

            await self.notification.create(
                user_id=member.student.user_id,
                title="Proposal Approved",
                message=f"Your proposal '{proposal.title}' has been approved.",
                type="Proposal",
            )

        return proposal

    # =====================================================
    # REJECT
    # =====================================================

    async def reject_proposal(
        self,
        current_user,
        proposal_id: UUID,
        feedback: str | None,
    ):
        professor = await self.repo.get_professor(
            current_user.id
        )

        if not professor:
            raise HTTPException(
                status_code=403,
                detail="Only professors can reject proposals.",
            )

        proposal = await self.repo.get_proposal(
            proposal_id
        )

        if not proposal:
            raise HTTPException(
                status_code=404,
                detail="Proposal not found.",
            )

        if proposal.professor_id != professor.id:
            raise HTTPException(
                status_code=403,
                detail="This proposal is not assigned to you.",
            )

        proposal.status = "Rejected"
        proposal.feedback = feedback

        await self.repo.update_proposal(
            proposal
        )

        await self.db.commit()

        for member in proposal.group.members:

            await self.notification.create(
                user_id=member.student.user_id,
                title="Proposal Rejected",
                message=(
                    f"Your proposal '{proposal.title}' was rejected."
                    f"\n\nFeedback:\n{feedback or 'No feedback provided.'}"
                ),
                type="Proposal",
            )

        return proposal