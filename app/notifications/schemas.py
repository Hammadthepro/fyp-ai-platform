from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


# =====================================================
# Notification
# =====================================================

class NotificationResponse(BaseModel):

    id: UUID

    title: str

    message: str

    type: str

    is_read: bool

    created_at: datetime


# =====================================================
# Create Notification
# =====================================================

class NotificationCreate(BaseModel):

    user_id: UUID

    title: str

    message: str

    type: str = "General"


# =====================================================
# Update Notification
# =====================================================

class NotificationUpdate(BaseModel):

    is_read: bool


# =====================================================
# Notification Count
# =====================================================

class NotificationCount(BaseModel):

    unread: int


# =====================================================
# Bulk Response
# =====================================================

class NotificationListResponse(BaseModel):

    notifications: list[NotificationResponse]