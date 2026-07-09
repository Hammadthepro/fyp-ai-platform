from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.student import Student
from app.models.professor import Professor
from app.models.group import Group
from app.models.group_member import GroupMember
from app.models.proposal import Proposal
from app.models.milestone import Milestone
from app.models.submission import Submission
from app.models.notification import Notification
from app.models.user import User
from app.models.fyp_idea import FYPIdea


class DashboardRepository:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    # ===================================================
    # STUDENT
    # ===================================================

    async def get_student(self, user_id):

        result = await self.db.execute(
            select(Student)
            .options(
                selectinload(Student.user),
                selectinload(Student.skills),
                selectinload(Student.domains),
            )
            .where(
                Student.user_id == user_id
            )
        )

        return result.scalar_one_or_none()

    async def get_student_group(self, student_id):

        result = await self.db.execute(
            select(Group)
            .join(
                GroupMember,
                Group.id == GroupMember.group_id,
            )
            .options(
                selectinload(Group.members)
                .selectinload(GroupMember.student)
            )
            .where(
                GroupMember.student_id == student_id
            )
        )

        return result.scalar_one_or_none()

    async def get_group_proposal(self, group_id):

        result = await self.db.execute(
            select(Proposal)
            .options(
                selectinload(Proposal.professor)
                .selectinload(Professor.user)
            )
            .where(
                Proposal.group_id == group_id
            )
        )

        return result.scalar_one_or_none()

    async def get_group_milestones(self, group_id):

        result = await self.db.execute(
            select(Milestone)
            .where(
                Milestone.group_id == group_id
            )
            .order_by(Milestone.due_date)
        )

        return result.scalars().all()

    async def get_group_submissions(self, group_id):

        result = await self.db.execute(
            select(Submission)
            .join(
                Milestone,
                Submission.milestone_id == Milestone.id,
            )
            .where(
                Milestone.group_id == group_id
            )
            .options(
                selectinload(Submission.student)
                .selectinload(Student.user),
                selectinload(Submission.milestone),
            )
        )

        return result.scalars().all()

    async def get_notifications(self, user_id):

        result = await self.db.execute(
            select(Notification)
            .where(
                Notification.user_id == user_id
            )
            .order_by(
                Notification.created_at.desc()
            )
            .limit(10)
        )

        return result.scalars().all()

        # ===================================================
    # PROFESSOR
    # ===================================================

    async def get_professor(
        self,
        user_id,
    ):
        result = await self.db.execute(
            select(Professor)
            .options(
                selectinload(
                    Professor.user
                )
            )
            .where(
                Professor.user_id == user_id
            )
        )

        return result.scalar_one_or_none()

    async def get_professor_proposals(
        self,
        professor_id,
    ):
        result = await self.db.execute(
            select(Proposal)
            .options(
                selectinload(
                    Proposal.group
                ),
                selectinload(
                    Proposal.professor
                ).selectinload(
                    Professor.user
                ),
            )
            .where(
                Proposal.professor_id == professor_id
            )
            .order_by(
                Proposal.created_at.desc()
            )
        )

        return result.scalars().all()

    async def get_professor_groups(
        self,
        professor_id,
    ):
        result = await self.db.execute(
            select(Group)
            .join(
                Proposal,
                Proposal.group_id == Group.id,
            )
            .where(
                Proposal.professor_id == professor_id,
                Proposal.status == "Approved",
            )
            .options(
                selectinload(
                    Group.members
                ).selectinload(
                    GroupMember.student
                )
            )
        )

        return result.scalars().unique().all()

    # ===================================================
    # ADMIN STATS
    # ===================================================

    async def total_students(self):
        result = await self.db.execute(
            select(
                func.count(Student.id)
            )
        )

        return result.scalar_one()

    async def total_professors(self):
        result = await self.db.execute(
            select(
                func.count(Professor.id)
            )
        )

        return result.scalar_one()

    async def total_groups(self):
        result = await self.db.execute(
            select(
                func.count(Group.id)
            )
        )

        return result.scalar_one()

    async def total_ideas(self):
        result = await self.db.execute(
            select(
                func.count(FYPIdea.id)
            )
        )

        return result.scalar_one()

    async def total_proposals(self):
        result = await self.db.execute(
            select(
                func.count(Proposal.id)
            )
        )

        return result.scalar_one()

    async def total_milestones(self):
        result = await self.db.execute(
            select(
                func.count(Milestone.id)
            )
        )

        return result.scalar_one()

    async def total_submissions(self):
        result = await self.db.execute(
            select(
                func.count(Submission.id)
            )
        )

        return result.scalar_one()


        # ===================================================
    # PROPOSAL STATS
    # ===================================================

    async def approved_proposals(self):
        result = await self.db.execute(
            select(
                func.count(Proposal.id)
            ).where(
                Proposal.status == "Approved"
            )
        )

        return result.scalar_one()

    async def pending_proposals(self):
        result = await self.db.execute(
            select(
                func.count(Proposal.id)
            ).where(
                Proposal.status == "Pending"
            )
        )

        return result.scalar_one()

    async def rejected_proposals(self):
        result = await self.db.execute(
            select(
                func.count(Proposal.id)
            ).where(
                Proposal.status == "Rejected"
            )
        )

        return result.scalar_one()

    # ===================================================
    # RECENT DATA
    # ===================================================

    async def recent_proposals(
        self,
        limit: int = 5,
    ):
        result = await self.db.execute(
            select(Proposal)
            .options(
                selectinload(
                    Proposal.group
                ),
                selectinload(
                    Proposal.professor
                ).selectinload(
                    Professor.user
                ),
            )
            .order_by(
                Proposal.created_at.desc()
            )
            .limit(limit)
        )

        return result.scalars().all()

    async def recent_groups(
        self,
        limit: int = 5,
    ):
        result = await self.db.execute(
            select(Group)
            .options(
                selectinload(
                    Group.members
                ).selectinload(
                    GroupMember.student
                )
            )
            .order_by(
                Group.created_at.desc()
            )
            .limit(limit)
        )

        return result.scalars().unique().all()

    async def recent_submissions(
        self,
        limit: int = 5,
    ):
        result = await self.db.execute(
            select(Submission)
            .options(
                selectinload(
                    Submission.student
                ).selectinload(
                    Student.user
                ),
                selectinload(
                    Submission.milestone
                ),
            )
            .order_by(
                Submission.created_at.desc()
            )
            .limit(limit)
        )

        return result.scalars().all()

    async def recent_users(
        self,
        limit: int = 5,
    ):
        result = await self.db.execute(
            select(User)
            .order_by(
                User.created_at.desc()
            )
            .limit(limit)
        )

        return result.scalars().all()

    # ===================================================
    # ADMIN DASHBOARD
    # ===================================================

    async def admin_dashboard(self):

        return {
            "students": await self.total_students(),
            "professors": await self.total_professors(),
            "groups": await self.total_groups(),
            "ideas": await self.total_ideas(),
            "proposals": await self.total_proposals(),
            "approved": await self.approved_proposals(),
            "pending": await self.pending_proposals(),
            "rejected": await self.rejected_proposals(),
            "milestones": await self.total_milestones(),
            "submissions": await self.total_submissions(),
            "recent_users": await self.recent_users(),
            "recent_groups": await self.recent_groups(),
            "recent_proposals": await self.recent_proposals(),
            "recent_submissions": await self.recent_submissions(),
        }