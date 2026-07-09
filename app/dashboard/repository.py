from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.group import Group
from app.models.milestone import Milestone
from app.models.professor import Professor
from app.models.proposal import Proposal
from app.models.student import Student
from app.models.submission import Submission


class DashboardRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_student(self, user_id: UUID):
        result = await self.db.execute(
            select(Student).where(
                Student.user_id == user_id
            )
        )
        return result.scalar_one_or_none()

    async def get_professor(self, user_id: UUID):
        result = await self.db.execute(
            select(Professor).where(
                Professor.user_id == user_id
            )
        )
        return result.scalar_one_or_none()

    async def get_student_group(self, student_id: UUID):
        result = await self.db.execute(
            select(Group).where(
                Group.leader_id == student_id
            )
        )
        return result.scalar_one_or_none()

    async def get_group_proposal(self, group_id: UUID):
        result = await self.db.execute(
            select(Proposal).where(
                Proposal.group_id == group_id
            )
        )
        return result.scalar_one_or_none()

    async def count_group_milestones(self, group_id: UUID):
        result = await self.db.execute(
            select(func.count(Milestone.id)).where(
                Milestone.group_id == group_id
            )
        )
        return result.scalar() or 0

    async def count_completed_milestones(self, group_id: UUID):
        result = await self.db.execute(
            select(func.count(Milestone.id)).where(
                Milestone.group_id == group_id,
                Milestone.status == "Completed",
            )
        )
        return result.scalar() or 0

    async def count_student_submissions(self, student_id: UUID):
        result = await self.db.execute(
            select(func.count(Submission.id)).where(
                Submission.submitted_by == student_id
            )
        )
        return result.scalar() or 0

    async def count_professor_groups(self, professor_id: UUID):
        result = await self.db.execute(
            select(func.count(Group.id)).where(
                Group.supervisor_id == professor_id
            )
        )
        return result.scalar() or 0

    async def count_professor_students(self, professor_id: UUID):
        result = await self.db.execute(
            select(func.count(Student.id))
            .join(Group, Group.leader_id == Student.id)
            .where(Group.supervisor_id == professor_id)
        )
        return result.scalar() or 0

    async def count_pending_proposals(self):
        result = await self.db.execute(
            select(func.count(Proposal.id)).where(
                Proposal.status == "Pending"
            )
        )
        return result.scalar() or 0

    async def count_pending_submissions(self):
        result = await self.db.execute(
            select(func.count(Submission.id)).where(
                Submission.status == "Submitted"
            )
        )
        return result.scalar() or 0

    async def count_total_milestones(self):
        result = await self.db.execute(
            select(func.count(Milestone.id))
        )
        return result.scalar() or 0