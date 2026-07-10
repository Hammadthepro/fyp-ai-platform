from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.chat.schemas import (
    ChatMessageCreate,
    ChatMessageResponse,
    ChatMessageUpdate,
    ChatRoomCreate,
    ChatRoomResponse,
)
from app.chat.service import ChatService
from app.database.database import get_db
from fastapi import WebSocket, WebSocketDisconnect
from app.chat.websocket import manager
from sqlalchemy import select

from app.core.security import decode_access_token
from app.models.user import User
from app.chat.websocket import manager
from app.chat.ws_service import ChatWebSocketService
from app.chat.repository import ChatRepository

router = APIRouter(
    prefix="/chat",
    tags=["Team Chat"],
)


# ==========================================
# CREATE ROOM
# ==========================================

@router.post(
    "/rooms",
    response_model=ChatRoomResponse,
)
async def create_room(
    data: ChatRoomCreate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = ChatService(db)

    return await service.create_room(
        data,
    )


# ==========================================
# SEND MESSAGE
# ==========================================

@router.post(
    "/messages",
    response_model=ChatMessageResponse,
)
async def send_message(
    data: ChatMessageCreate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = ChatService(db)

    return await service.send_message(
        current_user,
        data,
    )


# ==========================================
# GET ROOM MESSAGES
# ==========================================

@router.get(
    "/rooms/{room_id}/messages",
    response_model=list[ChatMessageResponse],
)
async def get_messages(
    room_id: UUID,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = ChatService(db)

    return await service.get_messages(
        current_user,
        room_id,
    )


# ==========================================
# UPDATE MESSAGE
# ==========================================

@router.put(
    "/messages/{message_id}",
    response_model=ChatMessageResponse,
)
async def update_message(
    message_id: UUID,
    data: ChatMessageUpdate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = ChatService(db)

    return await service.update_message(
        current_user,
        message_id,
        data,
    )


# ==========================================
# DELETE MESSAGE
# ==========================================

@router.delete(
    "/messages/{message_id}",
)
async def delete_message(
    message_id: UUID,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = ChatService(db)

    return await service.delete_message(
        current_user,
        message_id,
    )

@router.websocket("/ws/{room_id}")
async def websocket_chat(
    websocket: WebSocket,
    room_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    token = websocket.query_params.get("token")

    if not token:
        await websocket.close(code=1008)
        return

    payload = decode_access_token(token)

    if not payload:
        await websocket.close(code=1008)
        return

    user_id = payload.get("sub")

    result = await db.execute(
        select(User).where(
            User.id == user_id
        )
    )

    current_user = result.scalar_one_or_none()

    if not current_user:
        await websocket.close(code=1008)
        return

    repo = ChatRepository(db)

    room = await repo.get_room(room_id)

    if not room:
        await websocket.close(code=1008)
        return

    allowed = await repo.is_group_member(
        room.group_id,
        current_user.id,
    )

    role = str(current_user.role).lower()

    if not allowed and "admin" not in role:
        await websocket.close(code=1008)
        return

    await manager.connect(
        room_id,
        websocket,
    )

    ws_service = ChatWebSocketService(db)

    try:
        while True:

            text = await websocket.receive_text()

            message = await ws_service.save_message(
                room_id=room_id,
                sender_id=current_user.id,
                message=text,
            )

            await manager.broadcast(
                room_id,
                {
                    "id": str(message.id),
                    "room_id": str(room_id),
                    "sender_id": str(current_user.id),
                    "sender_name": current_user.full_name,
                    "message": message.message,
                    "created_at": message.created_at.isoformat(),
                },
            )

    except WebSocketDisconnect:

        manager.disconnect(
            room_id,
            websocket,
        )