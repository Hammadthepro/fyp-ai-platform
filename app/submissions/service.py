from uuid import UUID

from fastapi import HTTPException

from app.models.submission import Submission
from app.submissions.repository import SubmissionRepository


class SubmissionService:

    def __init__(self, db):
        self.db = db
        self.repo = SubmissionRepository(db)

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
        )

        await self.repo.create_submission(
            submission
        )

        await self.db.commit()
        await self.db.refresh(submission)

        return submission

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

    async def update_submission(
        self,
        current_user,
        submission_id: UUID,
        data,
    ):
        # Allow only professors/admins to review submissions
        role = str(current_user.role).lower()

        if "professor" not in role and "admin" not in role:
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

        return submission