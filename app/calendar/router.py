from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.calendar.schemas import (
    CalendarEventCreate,
    CalendarEventResponse,
    CalendarEventUpdate,
    UpcomingEventsResponse,
)
from app.calendar.service import CalendarService
from app.core.dependencies import get_current_user
from app.database.database import get_db
from app.models.user import User

router = APIRouter(
    prefix="/calendar",
    tags=["Calendar"],
)


# =====================================================
# CREATE EVENT
# =====================================================

@router.post(
    "/events",
    response_model=CalendarEventResponse,
)
async def create_event(
    data: CalendarEventCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = CalendarService(db)

    return await service.create_event(
        current_user,
        data,
    )


# =====================================================
# LIST EVENTS
# =====================================================

@router.get(
    "/events",
    response_model=list[CalendarEventResponse],
)
async def list_events(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = CalendarService(db)

    return await service.get_events(
        current_user,
    )


# =====================================================
# UPCOMING EVENTS
# =====================================================

@router.get(
    "/upcoming",
    response_model=UpcomingEventsResponse,
)
async def upcoming_events(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = CalendarService(db)

    events = await service.upcoming_events(
        current_user,
    )

    return {
        "upcoming_events": events
    }


# =====================================================
# UPDATE EVENT
# =====================================================

@router.put(
    "/events/{event_id}",
    response_model=CalendarEventResponse,
)
async def update_event(
    event_id: UUID,
    data: CalendarEventUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = CalendarService(db)

    return await service.update_event(
        event_id,
        data,
    )


# =====================================================
# DELETE EVENT
# =====================================================

@router.delete(
    "/events/{event_id}",
)
async def delete_event(
    event_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = CalendarService(db)

    return await service.delete_event(
        event_id,
    )


# =====================================================
# STUDENT CALENDAR
# =====================================================

@router.get("/student")
async def student_calendar(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = CalendarService(db)

    return await service.student_calendar(
        current_user,
    )


# =====================================================
# PROFESSOR CALENDAR
# =====================================================

@router.get("/professor")
async def professor_calendar(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = CalendarService(db)

    return await service.professor_calendar(
        current_user,
    )


# =====================================================
# ADMIN CALENDAR
# =====================================================

@router.get("/admin")
async def admin_calendar(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = CalendarService(db)

    return await service.admin_calendar(
        current_user,
    )