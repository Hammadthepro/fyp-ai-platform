from fastapi import HTTPException

from app.groups.repository import GroupRepository
from app.models.group import Group
from app.models.group_invitation import GroupInvitation


class GroupService:

    def __init__(self, db):
        self.db = db
        self.repo = GroupRepository(db)

    async def create_group(
        self,
        current_user,
        data,
    ):

        student = await self.repo.get_student(
            current_user.id
        )

        if not student:
            raise HTTPException(
                403,
                "Only students can create groups.",
            )

        existing = await self.repo.get_group_by_student(
            student.id
        )

        if existing:
            raise HTTPException(
                400,
                "Student already belongs to a group.",
            )

        group = Group(
            name=data.name,
            leader_id=student.id,
        )

        await self.repo.create_group(group)

        await self.repo.add_member(
            group.id,
            student.id,
        )

        await self.db.commit()

        return await self.repo.get_group(
            group.id
        )

    async def invite_student(
        self,
        current_user,
        group_id,
        data,
    ):

        # Logged-in student
        student = await self.repo.get_student(
            current_user.id
        )

        if not student:
            raise HTTPException(
                403,
                "Only students can invite members.",
            )

        # Group
        group = await self.repo.get_group(
            group_id
        )

        if not group:
            raise HTTPException(
                404,
                "Group not found.",
            )

        # Only leader can invite
        if group.leader_id != student.id:
            raise HTTPException(
                403,
                "Only the group leader can invite students.",
            )

        # Student being invited
        invited_student = await self.repo.get_student_by_id(
            data.student_id
        )

        if not invited_student:
            raise HTTPException(
                404,
                "Student not found.",
            )

        # Already in a group?
        existing_group = await self.repo.get_group_by_student(
            invited_student.id
        )

        if existing_group:
            raise HTTPException(
                400,
                "Student already belongs to a group.",
            )

        # Invitation already exists?
        invitation = await self.repo.get_pending_invitation(
            group.id,
            invited_student.id,
        )

        if invitation:
            raise HTTPException(
                400,
                "Invitation already sent.",
            )

        # Group full?
        member_count = await self.repo.count_members(
            group.id
        )

        if member_count >= 5:
            raise HTTPException(
                400,
                "Group is full.",
            )

        invitation = GroupInvitation(
            group_id=group.id,
            student_id=invited_student.id,
            status="Pending",
        )

        invitation = await self.repo.create_invitation(
            invitation
        )

        await self.db.commit()

        return invitation