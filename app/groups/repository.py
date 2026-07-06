from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.group import Group
from app.models.group_invitation import GroupInvitation
from app.models.group_member import GroupMember
from app.models.student import Student


class GroupRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_student(
        self,
        user_id: UUID,
    ):
        result = await self.db.execute(
            select(Student).where(
                Student.user_id == user_id
            )
        )

        return result.scalar_one_or_none()

    async def get_student_by_id(
        self,
        student_id: UUID,
    ):
        result = await self.db.execute(
            select(Student).where(
                Student.id == student_id
            )
        )

        return result.scalar_one_or_none()

    async def get_group_by_student(
        self,
        student_id: UUID,
    ):
        result = await self.db.execute(
            select(GroupMember).where(
                GroupMember.student_id == student_id
            )
        )

        return result.scalar_one_or_none()

    async def create_group(
        self,
        group: Group,
    ):
        self.db.add(group)

        await self.db.flush()
        await self.db.refresh(group)

        return group

    async def add_member(
        self,
        group_id: UUID,
        student_id: UUID,
    ):
        self.db.add(
            GroupMember(
                group_id=group_id,
                student_id=student_id,
            )
        )

    async def get_group(
        self,
        group_id: UUID,
    ):
        result = await self.db.execute(
            select(Group)
            .where(Group.id == group_id)
            .options(
                selectinload(Group.members)
                .selectinload(GroupMember.student)
            )
        )

        return result.scalar_one()

    async def get_pending_invitation(
        self,
        group_id: UUID,
        student_id: UUID,
    ):
        result = await self.db.execute(
            select(GroupInvitation).where(
                GroupInvitation.group_id == group_id,
                GroupInvitation.student_id == student_id,
                GroupInvitation.status == "Pending",
            )
        )

        return result.scalar_one_or_none()

    async def create_invitation(
        self,
        invitation: GroupInvitation,
    ):
        self.db.add(invitation)

        await self.db.flush()
        await self.db.refresh(invitation)

        return invitation

    async def get_invitation(
        self,
        invitation_id: UUID,
    ):
        result = await self.db.execute(
            select(GroupInvitation)
            .where(
                GroupInvitation.id == invitation_id
            )
            .options(
                selectinload(GroupInvitation.group),
                selectinload(GroupInvitation.student),
            )
        )

        return result.scalar_one_or_none()

    async def update_invitation(
        self,
        invitation: GroupInvitation,
    ):
        await self.db.flush()
        await self.db.refresh(invitation)

        return invitation

    async def count_members(
        self,
        group_id: UUID,
    ):
        result = await self.db.execute(
            select(
                func.count(GroupMember.id)
            ).where(
                GroupMember.group_id == group_id
            )
        )

        return result.scalar_one()