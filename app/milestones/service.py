from uuid import UUID

from fastapi import HTTPException

from app.groups.repository import GroupRepository
from app.milestones.repository import MilestoneRepository
from app.models.milestone import Milestone


class MilestoneService:

    def __init__(self, db):
        self.db = db
        self.repo = MilestoneRepository(db)
        self.group_repo = GroupRepository(db)

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

        return milestone

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

        return milestone

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

        await self.repo.delete_milestone(
            milestone
        )

        await self.db.commit()

        return {
            "message": "Milestone deleted successfully."
        }