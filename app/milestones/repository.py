from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.group import Group
from app.models.group_member import GroupMember
from app.models.milestone import Milestone
from app.models.student import Student


class MilestoneRepository:

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
    # CREATE
    # =====================================================

    async def create_milestone(
        self,
        milestone: Milestone,
    ):
        self.db.add(milestone)

        await self.db.flush()
        await self.db.refresh(milestone)

        return milestone

    # =====================================================
    # SINGLE
    # =====================================================

    async def get_milestone(
        self,
        milestone_id: UUID,
    ):
        result = await self.db.execute(
            select(Milestone)
            .options(
                selectinload(Milestone.group)
                .selectinload(Group.members)
                .selectinload(GroupMember.student)
                .selectinload(Student.user)
            )
            .where(
                Milestone.id == milestone_id
            )
        )

        return result.scalar_one_or_none()

    # =====================================================
    # GROUP MILESTONES
    # =====================================================

    async def get_group_milestones(
        self,
        group_id: UUID,
    ):
        result = await self.db.execute(
            select(Milestone)
            .where(
                Milestone.group_id == group_id
            )
            .order_by(
                Milestone.created_at
            )
        )

        return result.scalars().all()

    # =====================================================
    # UPDATE
    # =====================================================

    async def update_milestone(
        self,
        milestone: Milestone,
    ):
        await self.db.flush()
        await self.db.refresh(milestone)

        return milestone

    # =====================================================
    # DELETE
    # =====================================================

    async def delete_milestone(
        self,
        milestone: Milestone,
    ):
        await self.db.delete(milestone)