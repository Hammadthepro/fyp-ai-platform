from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.fyp_idea import FYPIdea
from app.models.group import Group
from app.models.group_member import GroupMember
from app.models.idea_skill import IdeaSkill
from app.models.idea_technology import IdeaTechnology
from app.models.milestone import Milestone
from app.models.professor import Professor
from app.models.proposal import Proposal
from app.models.student import Student
from app.models.student_domain import StudentDomain
from app.models.student_skill import StudentSkill
from app.models.submission import Submission
from app.models.user import User


class AIRepository:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    # =====================================================
    # USER
    # =====================================================

    async def get_user(
        self,
        user_id: UUID,
    ):
        result = await self.db.execute(
            select(User).where(
                User.id == user_id
            )
        )

        return result.scalar_one_or_none()

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
                selectinload(Student.user),
                selectinload(Student.skills)
                .selectinload(StudentSkill.skill),
                selectinload(Student.domains)
                .selectinload(StudentDomain.domain),
            )
            .where(
                Student.user_id == user_id
            )
        )

        return result.scalar_one_or_none()

    async def get_student_by_id(
        self,
        student_id: UUID,
    ):
        result = await self.db.execute(
            select(Student)
            .options(
                selectinload(Student.user),
                selectinload(Student.skills)
                .selectinload(StudentSkill.skill),
                selectinload(Student.domains)
                .selectinload(StudentDomain.domain),
            )
            .where(
                Student.id == student_id
            )
        )

        return result.scalar_one_or_none()

    # =====================================================
    # PROFESSOR
    # =====================================================

    async def get_professor(
        self,
        user_id: UUID,
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

    async def get_professor_by_id(
        self,
        professor_id: UUID,
    ):
        result = await self.db.execute(
            select(Professor)
            .options(
                selectinload(
                    Professor.user
                )
            )
            .where(
                Professor.id == professor_id
            )
        )

        return result.scalar_one_or_none()

    # =====================================================
    # IDEAS
    # =====================================================

    async def get_all_ideas(
        self,
    ):
        result = await self.db.execute(
            select(FYPIdea)
            .options(
                selectinload(
                    FYPIdea.domain
                ),
                selectinload(
                    FYPIdea.professor
                ),
                selectinload(
                    FYPIdea.skills
                ).selectinload(
                    IdeaSkill.skill
                ),
                selectinload(
                    FYPIdea.technologies
                ).selectinload(
                    IdeaTechnology.technology
                ),
            )
            .where(
                FYPIdea.is_active == True
            )
        )

        return result.scalars().unique().all()

    async def get_idea(
        self,
        idea_id: UUID,
    ):
        result = await self.db.execute(
            select(FYPIdea)
            .options(
                selectinload(
                    FYPIdea.domain
                ),
                selectinload(
                    FYPIdea.professor
                ),
                selectinload(
                    FYPIdea.skills
                ).selectinload(
                    IdeaSkill.skill
                ),
                selectinload(
                    FYPIdea.technologies
                ).selectinload(
                    IdeaTechnology.technology
                ),
            )
            .where(
                FYPIdea.id == idea_id
            )
        )

        return result.scalar_one_or_none()

    # =====================================================
    # GROUP
    # =====================================================

    async def get_group_of_student(
        self,
        student_id: UUID,
    ):
        result = await self.db.execute(
            select(Group)
            .join(
                GroupMember,
                Group.id == GroupMember.group_id,
            )
            .options(
                selectinload(
                    Group.members
                ).selectinload(
                    GroupMember.student
                )
            )
            .where(
                GroupMember.student_id == student_id
            )
        )

        return result.scalar_one_or_none()

    async def get_group(
        self,
        group_id: UUID,
    ):
        result = await self.db.execute(
            select(Group)
            .options(
                selectinload(
                    Group.members
                ).selectinload(
                    GroupMember.student
                ),
                selectinload(
                    Group.proposals
                ),
                selectinload(
                    Group.milestones
                ),
            )
            .where(
                Group.id == group_id
            )
        )

        return result.scalar_one_or_none()


    # =====================================================
    # PROPOSALS
    # =====================================================

    async def get_group_proposal(
        self,
        group_id: UUID,
    ):
        result = await self.db.execute(
            select(Proposal)
            .options(
                selectinload(
                    Proposal.professor
                ).selectinload(
                    Professor.user
                ),
                selectinload(
                    Proposal.group
                ),
            )
            .where(
                Proposal.group_id == group_id
            )
        )

        return result.scalar_one_or_none()

    async def get_proposal(
        self,
        proposal_id: UUID,
    ):
        result = await self.db.execute(
            select(Proposal)
            .options(
                selectinload(
                    Proposal.professor
                ).selectinload(
                    Professor.user
                ),
                selectinload(
                    Proposal.group
                ),
            )
            .where(
                Proposal.id == proposal_id
            )
        )

        return result.scalar_one_or_none()

    async def get_professor_proposals(
        self,
        professor_id: UUID,
    ):
        result = await self.db.execute(
            select(Proposal)
            .options(
                selectinload(
                    Proposal.group
                )
            )
            .where(
                Proposal.professor_id == professor_id
            )
        )

        return result.scalars().all()

    # =====================================================
    # MILESTONES
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
                Milestone.due_date
            )
        )

        return result.scalars().all()

    async def get_milestone(
        self,
        milestone_id: UUID,
    ):
        result = await self.db.execute(
            select(Milestone)
            .where(
                Milestone.id == milestone_id
            )
        )

        return result.scalar_one_or_none()

    # =====================================================
    # SUBMISSIONS
    # =====================================================

    async def get_submission(
        self,
        submission_id: UUID,
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
            .where(
                Submission.id == submission_id
            )
        )

        return result.scalar_one_or_none()

    async def get_group_submissions(
        self,
        group_id: UUID,
    ):
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
                selectinload(
                    Submission.student
                ).selectinload(
                    Student.user
                ),
                selectinload(
                    Submission.milestone
                ),
            )
        )

        return result.scalars().all()

    async def get_student_submissions(
        self,
        student_id: UUID,
    ):
        result = await self.db.execute(
            select(Submission)
            .options(
                selectinload(
                    Submission.milestone
                )
            )
            .where(
                Submission.submitted_by == student_id
            )
        )

        return result.scalars().all()



        # =====================================================
    # PROJECT CONTEXT
    # =====================================================

    async def build_project_context(
        self,
        user_id: UUID,
    ):
        """
        Returns the complete project context for AI.
        """

        student = await self.get_student(user_id)

        if not student:
            return None

        group = await self.get_group_of_student(
            student.id
        )

        proposal = None
        professor = None
        milestones = []
        submissions = []

        if group:

            proposal = await self.get_group_proposal(
                group.id
            )

            milestones = await self.get_group_milestones(
                group.id
            )

            submissions = await self.get_group_submissions(
                group.id
            )

            if proposal:
                professor = await self.get_professor_by_id(
                    proposal.professor_id
                )

        return {
            "student": student,
            "group": group,
            "proposal": proposal,
            "professor": professor,
            "milestones": milestones,
            "submissions": submissions,
        }

    # =====================================================
    # DASHBOARD STATS
    # =====================================================

    async def dashboard_stats(self):

        students = (
            await self.db.execute(
                select(func.count(Student.id))
            )
        ).scalar_one()

        professors = (
            await self.db.execute(
                select(func.count(Professor.id))
            )
        ).scalar_one()

        groups = (
            await self.db.execute(
                select(func.count(Group.id))
            )
        ).scalar_one()

        proposals = (
            await self.db.execute(
                select(func.count(Proposal.id))
            )
        ).scalar_one()

        approved = (
            await self.db.execute(
                select(func.count(Proposal.id))
                .where(
                    Proposal.status == "Approved"
                )
            )
        ).scalar_one()

        pending = (
            await self.db.execute(
                select(func.count(Proposal.id))
                .where(
                    Proposal.status == "Pending"
                )
            )
        ).scalar_one()

        milestones = (
            await self.db.execute(
                select(func.count(Milestone.id))
            )
        ).scalar_one()

        submissions = (
            await self.db.execute(
                select(func.count(Submission.id))
            )
        ).scalar_one()

        ideas = (
            await self.db.execute(
                select(func.count(FYPIdea.id))
            )
        ).scalar_one()

        return {
            "students": students,
            "professors": professors,
            "groups": groups,
            "ideas": ideas,
            "proposals": proposals,
            "approved_proposals": approved,
            "pending_proposals": pending,
            "milestones": milestones,
            "submissions": submissions,
        }

    # =====================================================
    # PROFESSOR CONTEXT
    # =====================================================

    async def professor_context(
        self,
        user_id: UUID,
    ):
        professor = await self.get_professor(
            user_id
        )

        if not professor:
            return None

        proposals = await self.get_professor_proposals(
            professor.id
        )

        return {
            "professor": professor,
            "proposals": proposals,
        }

    # =====================================================
    # IDEA ANALYTICS
    # =====================================================

    async def idea_statistics(self):

        ideas = await self.get_all_ideas()

        domain_stats = {}

        difficulty_stats = {
            "Easy": 0,
            "Medium": 0,
            "Hard": 0,
        }

        for idea in ideas:

            if idea.domain:
                name = idea.domain.name
                domain_stats[name] = (
                    domain_stats.get(name, 0) + 1
                )

            if idea.difficulty:
                difficulty_stats[
                    idea.difficulty
                ] = (
                    difficulty_stats.get(
                        idea.difficulty,
                        0,
                    )
                    + 1
                )

        return {
            "total_ideas": len(ideas),
            "domains": domain_stats,
            "difficulty": difficulty_stats,
        }

    # =====================================================
    # STUDENT ANALYTICS
    # =====================================================

    async def student_progress(
        self,
        user_id: UUID,
    ):
        context = await self.build_project_context(
            user_id
        )

        if not context:
            return None

        completed = 0

        for milestone in context["milestones"]:
            if milestone.status == "Completed":
                completed += 1

        total = len(
            context["milestones"]
        )

        percentage = 0

        if total:
            percentage = round(
                (completed / total) * 100,
                2,
            )

        return {
            "completed": completed,
            "total": total,
            "progress": percentage,
            "submission_count": len(
                context["submissions"]
            ),
        }


        # =====================================================
    # PROFESSOR GROUPS
    # =====================================================

    async def get_professor_groups(
        self,
        professor_id: UUID,
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
                selectinload(Group.members)
                .selectinload(GroupMember.student)
            )
        )

        return result.scalars().unique().all()

    # =====================================================
    # RECENT SUBMISSIONS
    # =====================================================

    async def recent_submissions(
        self,
        limit: int = 10,
    ):
        result = await self.db.execute(
            select(Submission)
            .options(
                selectinload(Submission.student)
                .selectinload(Student.user),
                selectinload(Submission.milestone),
            )
            .order_by(
                Submission.created_at.desc()
            )
            .limit(limit)
        )

        return result.scalars().all()

    # =====================================================
    # RECENT PROPOSALS
    # =====================================================

    async def recent_proposals(
        self,
        limit: int = 10,
    ):
        result = await self.db.execute(
            select(Proposal)
            .options(
                selectinload(Proposal.group),
                selectinload(Proposal.professor)
                .selectinload(Professor.user),
            )
            .order_by(
                Proposal.created_at.desc()
            )
            .limit(limit)
        )

        return result.scalars().all()

    # =====================================================
    # RECENT MILESTONES
    # =====================================================

    async def recent_milestones(
        self,
        limit: int = 10,
    ):
        result = await self.db.execute(
            select(Milestone)
            .order_by(
                Milestone.created_at.desc()
            )
            .limit(limit)
        )

        return result.scalars().all()

    # =====================================================
    # ALL PROFESSORS
    # =====================================================

    async def get_all_professors(
        self,
    ):
        result = await self.db.execute(
            select(Professor)
            .options(
                selectinload(
                    Professor.user
                )
            )
        )

        return result.scalars().all()

    # =====================================================
    # ALL STUDENTS
    # =====================================================

    async def get_all_students(
        self,
    ):
        result = await self.db.execute(
            select(Student)
            .options(
                selectinload(
                    Student.user
                )
            )
        )

        return result.scalars().all()