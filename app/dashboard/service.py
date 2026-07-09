from app.dashboard.repository import DashboardRepository


class DashboardService:

    def __init__(self, db):
        self.db = db
        self.repo = DashboardRepository(db)

    # =====================================================
    # STUDENT DASHBOARD
    # =====================================================

    async def student_dashboard(
        self,
        current_user,
    ):

        student = await self.repo.get_student(
            current_user.id
        )

        if not student:
            return None

        group = await self.repo.get_student_group(
            student.id
        )

        proposal = None
        milestones = []
        notifications = []
        submissions = []

        if group:

            proposal = await self.repo.get_group_proposal(
                group.id
            )

            milestones = await self.repo.get_group_milestones(
                group.id
            )

            submissions = await self.repo.get_group_submissions(
                group.id
            )

        notifications = await self.repo.get_notifications(
            current_user.id
        )

        total = len(milestones)

        completed = len(
            [
                m
                for m in milestones
                if m.status == "Completed"
            ]
        )

        progress = 0

        if total:
            progress = round(
                completed * 100 / total,
                2,
            )

        return {
            "student": student,
            "group": group,
            "proposal": proposal,
            "milestones": milestones,
            "notifications": notifications,
            "submissions": submissions,
            "progress": progress,
            "completed": completed,
            "total": total,
        }


        # =====================================================
    # PROFESSOR DASHBOARD
    # =====================================================

    async def professor_dashboard(
        self,
        current_user,
    ):

        professor = await self.repo.get_professor(
            current_user.id
        )

        if not professor:
            return None

        proposals = await self.repo.get_professor_proposals(
            professor.id
        )

        groups = await self.repo.get_professor_groups(
            professor.id
        )

        pending = len(
            [
                p
                for p in proposals
                if p.status == "Pending"
            ]
        )

        approved = len(
            [
                p
                for p in proposals
                if p.status == "Approved"
            ]
        )

        rejected = len(
            [
                p
                for p in proposals
                if p.status == "Rejected"
            ]
        )

        return {
            "professor": professor,
            "groups": groups,
            "proposals": proposals,
            "total_groups": len(groups),
            "total_proposals": len(proposals),
            "pending": pending,
            "approved": approved,
            "rejected": rejected,
        }

        # =====================================================
    # ADMIN DASHBOARD
    # =====================================================

    async def admin_dashboard(
        self,
    ):
        return await self.repo.admin_dashboard()

    # =====================================================
    # DASHBOARD ANALYTICS
    # =====================================================

    async def analytics(
        self,
    ):

        dashboard = await self.repo.admin_dashboard()

        return {
            "dashboard": {
                "students": dashboard["students"],
                "professors": dashboard["professors"],
                "groups": dashboard["groups"],
                "ideas": dashboard["ideas"],
                "proposals": dashboard["proposals"],
                "approved": dashboard["approved"],
                "pending": dashboard["pending"],
                "rejected": dashboard["rejected"],
                "milestones": dashboard["milestones"],
                "submissions": dashboard["submissions"],
            },

            "recent_users": [
                {
                    "id": user.id,
                    "name": user.full_name,
                    "email": user.email,
                    "role": user.role.value,
                }
                for user in dashboard["recent_users"]
            ],

            "recent_groups": [
                {
                    "id": group.id,
                    "name": group.name,
                }
                for group in dashboard["recent_groups"]
            ],

            "recent_proposals": [
                {
                    "id": proposal.id,
                    "title": proposal.title,
                    "status": proposal.status,
                }
                for proposal in dashboard["recent_proposals"]
            ],

            "recent_submissions": [
                {
                    "id": submission.id,
                    "student": submission.student.user.full_name,
                    "milestone": submission.milestone.title,
                }
                for submission in dashboard["recent_submissions"]
            ],
        }