from datetime import datetime, timedelta
from uuid import UUID

from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.calendar_event import CalendarEvent
from app.models.group import Group
from app.models.group_member import GroupMember
from app.models.professor import Professor
from app.models.student import Student


class CalendarRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    # =====================================================
    # USER
    # =====================================================

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

    async def get_professor(
        self,
        user_id: UUID,
    ):
        result = await self.db.execute(
            select(Professor).where(
                Professor.user_id == user_id
            )
        )

        return result.scalar_one_or_none()

    # =====================================================
    # GROUPS
    # =====================================================

    async def get_student_groups(
        self,
        student_id: UUID,
    ):
        result = await self.db.execute(
            select(Group)
            .join(
                GroupMember,
                Group.id == GroupMember.group_id,
            )
            .where(
                GroupMember.student_id == student_id
            )
        )

        return result.scalars().all()

    async def get_professor_groups(
        self,
        professor_id: UUID,
    ):
        result = await self.db.execute(
            select(Group)
            .where(
                Group.supervisor_id == professor_id
            )
        )

        return result.scalars().all()
    # =====================================================
    # EVENTS
    # =====================================================

    async def create_event(
        self,
        event: CalendarEvent,
    ):
        self.db.add(event)

        await self.db.flush()
        await self.db.refresh(event)

        return event

    async def get_event(
        self,
        event_id: UUID,
    ):
        result = await self.db.execute(
            select(CalendarEvent)
            .options(
                selectinload(CalendarEvent.group),
                selectinload(CalendarEvent.creator),
            )
            .where(
                CalendarEvent.id == event_id
            )
        )

        return result.scalar_one_or_none()

    async def update_event(
        self,
        event: CalendarEvent,
    ):
        await self.db.flush()
        await self.db.refresh(event)

        return event

    async def delete_event(
        self,
        event: CalendarEvent,
    ):
        await self.db.delete(event)

    # =====================================================
    # LIST
    # =====================================================

    async def get_events_for_user(
        self,
        user_id: UUID,
    ):
        result = await self.db.execute(
            select(CalendarEvent)
            .options(
                selectinload(CalendarEvent.group),
                selectinload(CalendarEvent.creator),
            )
            .where(
                or_(
                    CalendarEvent.created_by == user_id,
                    CalendarEvent.group_id.is_not(None),
                )
            )
            .order_by(
                CalendarEvent.start_date
            )
        )

        return result.scalars().all()

    async def upcoming_events(
        self,
        user_id: UUID,
    ):
        now = datetime.utcnow()
        next_week = now + timedelta(days=7)

        result = await self.db.execute(
            select(CalendarEvent)
            .where(
                and_(
                    CalendarEvent.start_date >= now,
                    CalendarEvent.start_date <= next_week,
                    CalendarEvent.created_by == user_id,
                )
            )
            .order_by(
                CalendarEvent.start_date
            )
        )

        return result.scalars().all()