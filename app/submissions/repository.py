from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.group import Group
from app.models.group_member import GroupMember
from app.models.milestone import Milestone
from app.models.professor import Professor
from app.models.student import Student
from app.models.submission import Submission


class SubmissionRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    # =====================================================
    # STUDENT
    # =====================================================

    async def get_student(
        self,
        user_id: UUID,
    ):
        result = await self.db.execute(
            select(Student)
            .options(
                selectinload(Student.user)
            )
            .where(
                Student.user_id == user_id
            )
        )

        return result.scalar_one_or_none()

    # =====================================================
    # MILESTONE
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
                .selectinload(Student.user),

                selectinload(Milestone.group)
                .selectinload(Group.proposals)
                .selectinload(Professor.user),
            )
            .where(
                Milestone.id == milestone_id
            )
        )

        return result.scalar_one_or_none()

    # =====================================================
    # CREATE
    # =====================================================

    async def create_submission(
        self,
        submission: Submission,
    ):
        self.db.add(submission)

        await self.db.flush()
        await self.db.refresh(submission)

        return submission

    # =====================================================
    # SINGLE
    # =====================================================

    async def get_submission(
        self,
        milestone_id: UUID,
        student_id: UUID,
    ):
        result = await self.db.execute(
            select(Submission)
            .where(
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
            select(Submission)
            .options(
                selectinload(Submission.student)
                .selectinload(Student.user),

                selectinload(Submission.milestone)
                .selectinload(Milestone.group)
                .selectinload(Group.members)
                .selectinload(GroupMember.student)
                .selectinload(Student.user),

                selectinload(Submission.milestone)
                .selectinload(Milestone.group)
                .selectinload(Group.proposals)
                .selectinload(Professor.user),
            )
            .where(
                Submission.id == submission_id
            )
        )

        return result.scalar_one_or_none()

    # =====================================================
    # LIST
    # =====================================================

    async def get_submissions(
        self,
        milestone_id: UUID,
    ):
        result = await self.db.execute(
            select(Submission)
            .options(
                selectinload(Submission.student)
                .selectinload(Student.user)
            )
            .where(
                Submission.milestone_id == milestone_id
            )
        )

        return result.scalars().all()

    # =====================================================
    # UPDATE
    # =====================================================

    async def update_submission(
        self,
        submission: Submission,
    ):
        await self.db.flush()
        await self.db.refresh(submission)

        return submission