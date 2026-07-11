from uuid import UUID

from fastapi import HTTPException

from app.groups.repository import GroupRepository
from app.milestones.repository import MilestoneRepository
from app.models.milestone import Milestone
from app.notifications.service import NotificationService


class MilestoneService:

    def __init__(self, db):
        self.db = db
        self.repo = MilestoneRepository(db)
        self.group_repo = GroupRepository(db)
        self.notification = NotificationService(db)

    # =====================================================
    # CREATE
    # =====================================================

    async def create_milestone(
        self,
        current_user,
        group_id: UUID,
        data,
    ):
        professor = await self.group_repo.get_professor(
            current_user.id
        )

        if not professor:
            raise HTTPException(
                status_code=403,
                detail="Only professors can create milestones.",
            )

        group = await self.repo.get_group(
            group_id
        )

        if not group:
            raise HTTPException(
                status_code=404,
                detail="Group not found.",
            )

        milestone = Milestone(
            group_id=group_id,
            title=data.title,
            description=data.description,
            due_date=data.due_date,
            status="Pending",
        )

        await self.repo.create_milestone(
            milestone
        )

        await self.db.commit()

        # Notify all group members
        for member in group.members:

            await self.notification.create(
                user_id=member.student.user_id,
                title="New Milestone",
                message=(
                    f"A new milestone '{milestone.title}' "
                    f"has been assigned.\n"
                    f"Due Date: {milestone.due_date}"
                ),
                type="Milestone",
            )

        return milestone

    # =====================================================
    # LIST
    # =====================================================

    async def get_group_milestones(
        self,
        group_id: UUID,
    ):
        group = await self.repo.get_group(
            group_id
        )

        if not group:
            raise HTTPException(
                status_code=404,
                detail="Group not found.",
            )

        return await self.repo.get_group_milestones(
            group_id
        )

    # =====================================================
    # UPDATE
    # =====================================================

    async def update_milestone(
        self,
        milestone_id: UUID,
        data,
    ):
        milestone = await self.repo.get_milestone(
            milestone_id
        )

        if not milestone:
            raise HTTPException(
                status_code=404,
                detail="Milestone not found.",
            )

        for field, value in data.model_dump(
            exclude_unset=True
        ).items():

            setattr(
                milestone,
                field,
                value,
            )

        await self.repo.update_milestone(
            milestone
        )

        await self.db.commit()

        # Notify all group members
        for member in milestone.group.members:

            await self.notification.create(
                user_id=member.student.user_id,
                title="Milestone Updated",
                message=(
                    f"Milestone '{milestone.title}' "
                    "has been updated."
                ),
                type="Milestone",
            )

        return milestone

    # =====================================================
    # DELETE
    # =====================================================

    async def delete_milestone(
        self,
        milestone_id: UUID,
    ):
        milestone = await self.repo.get_milestone(
            milestone_id
        )

        if not milestone:
            raise HTTPException(
                status_code=404,
                detail="Milestone not found.",
            )

        members = milestone.group.members

        title = milestone.title

        await self.repo.delete_milestone(
            milestone
        )

        await self.db.commit()

        # Notify all group members
        for member in members:

            await self.notification.create(
                user_id=member.student.user_id,
                title="Milestone Deleted",
                message=(
                    f"The milestone '{title}' "
                    "has been removed."
                ),
                type="Milestone",
            )

        return {
            "message": "Milestone deleted successfully."
        }