from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.group import Group
from app.models.milestone import Milestone


class MilestoneRepository:

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

    async def create_milestone(
        self,
        milestone: Milestone,
    ):
        self.db.add(milestone)

        await self.db.flush()
        await self.db.refresh(milestone)

        return milestone

    async def get_milestone(
        self,
        milestone_id: UUID,
    ):
        result = await self.db.execute(
            select(Milestone).where(
                Milestone.id == milestone_id
            )
        )

        return result.scalar_one_or_none()

    async def get_group_milestones(
        self,
        group_id: UUID,
    ):
        result = await self.db.execute(
            select(Milestone)
            .where(
                Milestone.group_id == group_id
            )
            .order_by(Milestone.created_at)
        )

        return result.scalars().all()

    async def update_milestone(
        self,
        milestone: Milestone,
    ):
        await self.db.flush()
        await self.db.refresh(milestone)

        return milestone

    async def delete_milestone(
        self,
        milestone: Milestone,
    ):
        await self.db.delete(milestone)