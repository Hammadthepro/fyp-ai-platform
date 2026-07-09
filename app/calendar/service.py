from uuid import UUID

from fastapi import HTTPException

from app.calendar.repository import CalendarRepository
from app.models.calendar_event import CalendarEvent
from app.notifications.service import NotificationService


class CalendarService:

    def __init__(self, db):
        self.db = db
        self.repo = CalendarRepository(db)
        self.notification = NotificationService(db)

    # =====================================================
    # CREATE EVENT
    # =====================================================

    async def create_event(
        self,
        current_user,
        data,
    ):
        event = CalendarEvent(
            title=data.title,
            description=data.description,
            event_type=data.event_type,
            start_date=data.start_date,
            end_date=data.end_date,
            group_id=data.group_id,
            is_all_day=data.is_all_day,
            created_by=current_user.id,
        )

        await self.repo.create_event(event)

        await self.db.commit()

        await self.notification.create(
            user_id=current_user.id,
            title="Calendar Event",
            message=f"{event.title} has been added to your calendar.",
            type="Calendar",
        )

        return event

        # =====================================================
    # UPDATE EVENT
    # =====================================================

    async def update_event(
        self,
        event_id: UUID,
        data,
    ):
        event = await self.repo.get_event(
            event_id
        )

        if not event:
            raise HTTPException(
                status_code=404,
                detail="Event not found.",
            )

        for field, value in data.model_dump(
            exclude_unset=True
        ).items():

            setattr(
                event,
                field,
                value,
            )

        await self.repo.update_event(
            event
        )

        await self.db.commit()

        return event

    # =====================================================
    # DELETE EVENT
    # =====================================================

    async def delete_event(
        self,
        event_id: UUID,
    ):
        event = await self.repo.get_event(
            event_id
        )

        if not event:
            raise HTTPException(
                status_code=404,
                detail="Event not found.",
            )

        await self.repo.delete_event(
            event
        )

        await self.db.commit()

        return {
            "message": "Event deleted successfully."
        }

        # =====================================================
    # GET ALL EVENTS
    # =====================================================

    async def get_events(
        self,
        current_user,
    ):
        return await self.repo.get_events_for_user(
            current_user.id
        )

    # =====================================================
    # UPCOMING EVENTS
    # =====================================================

    async def upcoming_events(
        self,
        current_user,
    ):
        return await self.repo.upcoming_events(
            current_user.id
        )

    # =====================================================
    # STUDENT CALENDAR
    # =====================================================

    async def student_calendar(
        self,
        current_user,
    ):
        student = await self.repo.get_student(
            current_user.id
        )

        if not student:
            raise HTTPException(
                status_code=403,
                detail="Only students can access this calendar.",
            )

        return await self.repo.get_events_for_user(
            current_user.id
        )

    # =====================================================
    # PROFESSOR CALENDAR
    # =====================================================

    async def professor_calendar(
        self,
        current_user,
    ):
        professor = await self.repo.get_professor(
            current_user.id
        )

        if not professor:
            raise HTTPException(
                status_code=403,
                detail="Only professors can access this calendar.",
            )

        return await self.repo.get_events_for_user(
            current_user.id
        )

    # =====================================================
    # ADMIN CALENDAR
    # =====================================================

    async def admin_calendar(
        self,
        current_user,
    ):
        role = str(current_user.role).lower()

        if "admin" not in role:
            raise HTTPException(
                status_code=403,
                detail="Only admins can access this calendar.",
            )

        return await self.repo.get_events_for_user(
            current_user.id
        )

        # =====================================================
    # AUTO EVENTS
    # =====================================================

    async def create_milestone_event(
        self,
        milestone,
        created_by,
    ):
        """
        Automatically create a calendar event when a
        milestone is created.
        """

        event = CalendarEvent(
            title=f"Milestone: {milestone.title}",
            description=milestone.description,
            event_type="Milestone",
            start_date=milestone.due_date,
            end_date=milestone.due_date,
            group_id=milestone.group_id,
            created_by=created_by,
            is_all_day=False,
        )

        await self.repo.create_event(event)
        await self.db.commit()

        return event

    async def create_proposal_meeting(
        self,
        title,
        description,
        meeting_date,
        group_id,
        created_by,
    ):
        """
        Schedule proposal discussion.
        """

        event = CalendarEvent(
            title=title,
            description=description,
            event_type="Proposal",
            start_date=meeting_date,
            end_date=meeting_date,
            group_id=group_id,
            created_by=created_by,
        )

        await self.repo.create_event(event)
        await self.db.commit()

        return event

    async def create_presentation_event(
        self,
        title,
        presentation_date,
        group_id,
        created_by,
    ):
        """
        Schedule final presentation.
        """

        event = CalendarEvent(
            title=title,
            description="Final Project Presentation",
            event_type="Presentation",
            start_date=presentation_date,
            end_date=presentation_date,
            group_id=group_id,
            created_by=created_by,
        )

        await self.repo.create_event(event)
        await self.db.commit()

        return event

    async def create_deadline_reminder(
        self,
        title,
        reminder_date,
        group_id,
        created_by,
    ):
        """
        Create reminder event.
        """

        event = CalendarEvent(
            title=title,
            description="Automatic reminder",
            event_type="Reminder",
            start_date=reminder_date,
            end_date=reminder_date,
            group_id=group_id,
            created_by=created_by,
        )

        await self.repo.create_event(event)
        await self.db.commit()

        return event

        # =====================================================
    # AUTO EVENTS
    # =====================================================

    async def create_milestone_event(
        self,
        milestone,
        created_by,
    ):
        """
        Automatically create a calendar event when a
        milestone is created.
        """

        event = CalendarEvent(
            title=f"Milestone: {milestone.title}",
            description=milestone.description,
            event_type="Milestone",
            start_date=milestone.due_date,
            end_date=milestone.due_date,
            group_id=milestone.group_id,
            created_by=created_by,
            is_all_day=False,
        )

        await self.repo.create_event(event)
        await self.db.commit()

        return event

    async def create_proposal_meeting(
        self,
        title,
        description,
        meeting_date,
        group_id,
        created_by,
    ):
        """
        Schedule proposal discussion.
        """

        event = CalendarEvent(
            title=title,
            description=description,
            event_type="Proposal",
            start_date=meeting_date,
            end_date=meeting_date,
            group_id=group_id,
            created_by=created_by,
        )

        await self.repo.create_event(event)
        await self.db.commit()

        return event

    async def create_presentation_event(
        self,
        title,
        presentation_date,
        group_id,
        created_by,
    ):
        """
        Schedule final presentation.
        """

        event = CalendarEvent(
            title=title,
            description="Final Project Presentation",
            event_type="Presentation",
            start_date=presentation_date,
            end_date=presentation_date,
            group_id=group_id,
            created_by=created_by,
        )

        await self.repo.create_event(event)
        await self.db.commit()

        return event

    async def create_deadline_reminder(
        self,
        title,
        reminder_date,
        group_id,
        created_by,
    ):
        """
        Create reminder event.
        """

        event = CalendarEvent(
            title=title,
            description="Automatic reminder",
            event_type="Reminder",
            start_date=reminder_date,
            end_date=reminder_date,
            group_id=group_id,
            created_by=created_by,
        )

        await self.repo.create_event(event)
        await self.db.commit()

        return event