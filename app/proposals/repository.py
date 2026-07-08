from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.group import Group
from app.models.professor import Professor
from app.models.proposal import Proposal


class ProposalRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_group(
        self,
        group_id: UUID,
    ):
        result = await self.db.execute(
            select(Group).where(
                Group.id == group_id
            )
        )

        return result.scalar_one_or_none()

    async def get_professor(
        self,
        user_id: UUID,
    ):
        result = await self.db.execute(
            select(Professor).where(
                Professor.user_id == user_id
            )
        )

        return result.scalar_one_or_none()

    async def create_proposal(
        self,
        proposal: Proposal,
    ):
        self.db.add(proposal)

        await self.db.flush()
        await self.db.refresh(proposal)

        return proposal

    async def get_group_proposal(
        self,
        group_id: UUID,
    ):
        result = await self.db.execute(
            select(Proposal).where(
                Proposal.group_id == group_id
            )
        )

        return result.scalar_one_or_none()

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

    async def get_proposal(
        self,
        proposal_id: UUID,
    ):
        result = await self.db.execute(
            select(Proposal).where(
                Proposal.id == proposal_id
            )
        )

        return result.scalar_one_or_none()

    async def update_proposal(
        self,
        proposal: Proposal,
    ):
        await self.db.flush()
        await self.db.refresh(proposal)

        return proposal