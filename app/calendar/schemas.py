from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


# =====================================================
# CREATE
# =====================================================

class CalendarEventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    event_type: str = "General"
    start_date: datetime
    end_date: Optional[datetime] = None
    group_id: Optional[UUID] = None
    is_all_day: bool = False


# =====================================================
# UPDATE
# =====================================================

class CalendarEventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    event_type: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_all_day: Optional[bool] = None


# =====================================================
# RESPONSE
# =====================================================

class CalendarEventResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    event_type: str
    start_date: datetime
    end_date: Optional[datetime]
    is_all_day: bool
    group_id: Optional[UUID]
    created_by: UUID
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


# =====================================================
# UPCOMING
# =====================================================

class UpcomingEventsResponse(BaseModel):
    upcoming_events: list[CalendarEventResponse]