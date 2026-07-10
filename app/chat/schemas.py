from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


# ==========================================
# CREATE ROOM
# ==========================================

class ChatRoomCreate(BaseModel):
    group_id: UUID
    name: str


# ==========================================
# ROOM RESPONSE
# ==========================================

class ChatRoomResponse(BaseModel):
    id: UUID
    group_id: UUID
    name: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


# ==========================================
# SEND MESSAGE
# ==========================================

class ChatMessageCreate(BaseModel):
    room_id: UUID
    message: str


# ==========================================
# UPDATE MESSAGE
# ==========================================

class ChatMessageUpdate(BaseModel):
    message: str


# ==========================================
# RESPONSE
# ==========================================

class ChatMessageResponse(BaseModel):
    id: UUID
    room_id: UUID
    sender_id: UUID
    message: str
    is_ai: bool
    created_at: datetime

    model_config = {
        "from_attributes": True
    }