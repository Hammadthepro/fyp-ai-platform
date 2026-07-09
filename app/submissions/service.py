from uuid import UUID

from fastapi import HTTPException

from app.models.submission import Submission
from app.notifications.service import NotificationService
from app.submissions.repository import SubmissionRepository


class SubmissionService:

    def __init__(self, db):
        self.db = db
        self.repo = SubmissionRepository(db)
        self.notification = NotificationService(db)

    # =====================================================
    # SUBMIT
    # =====================================================

    async def submit(
        self,
        current_user,
        data,
    ):
        student = await self.repo.get_student(
            current_user.id
        )

        if not student:
            raise HTTPException(
                status_code=403,
                detail="Only students can submit milestones.",
            )

        milestone = await self.repo.get_milestone(
            data.milestone_id
        )

        if not milestone:
            raise HTTPException(
                status_code=404,
                detail="Milestone not found.",
            )

        existing = await self.repo.get_submission(
            data.milestone_id,
            student.id,
        )

        if existing:
            raise HTTPException(
                status_code=400,
                detail="You have already submitted this milestone.",
            )

        submission = Submission(
            milestone_id=data.milestone_id,
            submitted_by=student.id,
            github_link=data.github_link,
            drive_link=data.drive_link,
            notes=data.notes,
            status="Submitted",
        )

        await self.repo.create_submission(
            submission
        )

        await self.db.commit()
        await self.db.refresh(submission)

        # --------------------------------------------
        # Notify supervisor
        # --------------------------------------------

        if milestone.group.proposals:

            proposal = milestone.group.proposals[0]

            if proposal.professor:

                await self.notification.create(
                    user_id=proposal.professor.user_id,
                    title="New Submission",
                    message=(
                        f"{student.user.full_name} submitted "
                        f"'{milestone.title}'."
                    ),
                    type="Submission",
                )

        return submission

    # =====================================================
    # LIST
    # =====================================================

    async def get_submissions(
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

        return await self.repo.get_submissions(
            milestone_id
        )

    # =====================================================
    # REVIEW
    # =====================================================

    async def update_submission(
        self,
        current_user,
        submission_id: UUID,
        data,
    ):
        role = str(current_user.role).lower()

        if (
            "professor" not in role
            and "admin" not in role
        ):
            raise HTTPException(
                status_code=403,
                detail="Only professors can review submissions.",
            )

        submission = await self.repo.get_submission_by_id(
            submission_id
        )

        if not submission:
            raise HTTPException(
                status_code=404,
                detail="Submission not found.",
            )

        submission.status = data.status

        if data.feedback is not None:
            submission.feedback = data.feedback

        if data.marks is not None:
            submission.marks = data.marks

        await self.repo.update_submission(
            submission
        )

        await self.db.commit()
        await self.db.refresh(submission)

        # --------------------------------------------
        # Notify student
        # --------------------------------------------

        await self.notification.create(
            user_id=submission.student.user_id,
            title="Submission Reviewed",
            message=(
                f"Your submission for "
                f"'{submission.milestone.title}' "
                f"has been reviewed.\n"
                f"Status: {submission.status}"
            ),
            type="Submission",
        )

        return submission