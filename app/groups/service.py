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
        student_id,
    ):
        leader = await self.repo.get_student(
            current_user.id
        )

        if not leader:
            raise HTTPException(
                403,
                "Only students can invite.",
            )

        group = await self.repo.get_group(group_id)

        if group.leader_id != leader.id:
            raise HTTPException(
                403,
                "Only group leader can invite.",
            )

        if await self.repo.get_group_membership(student_id):
            raise HTTPException(
                400,
                "Student already belongs to a group.",
            )

        if await self.repo.get_pending_invitation(
            group_id,
            student_id,
        ):
            raise HTTPException(
                400,
                "Invitation already exists.",
            )

        invitation = GroupInvitation(
            group_id=group_id,
            student_id=student_id,
            status="Pending",
        )

        await self.repo.create_invitation(
            invitation
        )

        await self.db.commit()

        return invitation

    async def respond_to_invitation(
        self,
        current_user,
        invitation_id,
        action,
    ):
        student = await self.repo.get_student(
            current_user.id
        )

        if not student:
            raise HTTPException(
                403,
                "Only students can respond.",
            )

        invitation = await self.repo.get_invitation(
            invitation_id
        )

        if not invitation:
            raise HTTPException(
                404,
                "Invitation not found.",
            )

        if invitation.student_id != student.id:
            raise HTTPException(
                403,
                "This invitation is not yours.",
            )

        if invitation.status != "Pending":
            raise HTTPException(
                400,
                "Invitation already processed.",
            )

        action = action.lower()

        if action == "accept":

            members = await self.repo.count_members(
                invitation.group_id
            )

            if members >= 4:
                raise HTTPException(
                    400,
                    "Group is already full.",
                )

            if await self.repo.get_group_membership(
                student.id
            ):
                raise HTTPException(
                    400,
                    "Student already belongs to a group.",
                )

            await self.repo.add_member(
                invitation.group_id,
                student.id,
            )

            invitation.status = "Accepted"

        elif action == "reject":

            invitation.status = "Rejected"

        else:
            raise HTTPException(
                400,
                "Action must be accept or reject.",
            )

        await self.repo.update_invitation(
            invitation
        )

        await self.db.commit()

        return invitation