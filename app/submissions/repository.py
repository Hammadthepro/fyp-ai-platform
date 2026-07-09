from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.milestone import Milestone
from app.models.student import Student
from app.models.submission import Submission


class SubmissionRepository:

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

    async def create_submission(
        self,
        submission: Submission,
    ):
        self.db.add(submission)

        await self.db.flush()
        await self.db.refresh(submission)

        return submission

    async def get_submission(
        self,
        milestone_id: UUID,
        student_id: UUID,
    ):
        result = await self.db.execute(
            select(Submission).where(
                Submission.milestone_id == milestone_id,
                Submission.submitted_by == student_id,
            )
        )

        return result.scalar_one_or_none()

    async def get_submission_by_id(
        self,
        submission_id: UUID,
    ):
        result = await self.db.execute(
            select(Submission).where(
                Submission.id == submission_id
            )
        )

        return result.scalar_one_or_none()

    async def get_submissions(
        self,
        milestone_id: UUID,
    ):
        result = await self.db.execute(
            select(Submission).where(
                Submission.milestone_id == milestone_id
            )
        )

        return result.scalars().all()

    async def update_submission(
        self,
        submission: Submission,
    ):
        await self.db.flush()
        await self.db.refresh(submission)

        return submission