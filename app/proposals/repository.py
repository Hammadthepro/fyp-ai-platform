from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.group import Group
from app.models.group_member import GroupMember
from app.models.professor import Professor
from app.models.proposal import Proposal
from app.models.student import Student


class ProposalRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    # =====================================================
    # GROUP
    # =====================================================

    async def get_group(
        self,
        group_id: UUID,
    ):
        result = await self.db.execute(
            select(Group)
            .options(
                selectinload(Group.members)
                .selectinload(GroupMember.student)
                .selectinload(Student.user)
            )
            .where(
                Group.id == group_id
            )
        )

        return result.scalar_one_or_none()

    # =====================================================
    # PROFESSOR
    # =====================================================

    async def get_professor(
        self,
        user_id: UUID,
    ):
        result = await self.db.execute(
            select(Professor)
            .options(
                selectinload(Professor.user)
            )
            .where(
                Professor.user_id == user_id
            )
        )

        return result.scalar_one_or_none()

    # =====================================================
    # CREATE
    # =====================================================

    async def create_proposal(
        self,
        proposal: Proposal,
    ):
        self.db.add(proposal)

        await self.db.flush()
        await self.db.refresh(proposal)

        return proposal

    # =====================================================
    # GROUP PROPOSAL
    # =====================================================

    async def get_group_proposal(
        self,
        group_id: UUID,
    ):
        result = await self.db.execute(
            select(Proposal)
            .where(
                Proposal.group_id == group_id
            )
        )

        return result.scalar_one_or_none()

    # =====================================================
    # PENDING
    # =====================================================

    async def get_pending_proposals(
        self,
        professor_id: UUID,
    ):
        result = await self.db.execute(
            select(Proposal)
            .where(
                Proposal.professor_id == professor_id,
                Proposal.status == "Pending",
            )
            .options(
                selectinload(Proposal.group)
            )
        )

        return result.scalars().all()

    # =====================================================
    # SINGLE
    # =====================================================

    async def get_proposal(
        self,
        proposal_id: UUID,
    ):
        result = await self.db.execute(
            select(Proposal)
            .options(
                selectinload(Proposal.group)
                .selectinload(Group.members)
                .selectinload(GroupMember.student)
                .selectinload(Student.user),

                selectinload(Proposal.professor)
                .selectinload(Professor.user),
            )
            .where(
                Proposal.id == proposal_id
            )
        )

        return result.scalar_one_or_none()

    # =====================================================
    # UPDATE
    # =====================================================

    async def update_proposal(
        self,
        proposal: Proposal,
    ):
        await self.db.flush()
        await self.db.refresh(proposal)

        return proposal

    async def get_professor_by_id(
        self,
        professor_id: UUID,
    ):
        result = await self.db.execute(
            select(Professor)
            .options(
                selectinload(Professor.user)
            )
            .where(
                Professor.id == professor_id
            )
        )

        return result.scalar_one_or_none()