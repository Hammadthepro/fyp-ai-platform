from collections import defaultdict

from fastapi import WebSocket, WebSocketDisconnect


class ConnectionManager:

    def __init__(self):
        self.rooms: dict[str, list[WebSocket]] = defaultdict(list)

    async def connect(
        self,
        room_id: str,
        websocket: WebSocket,
    ):
        await websocket.accept()

        self.rooms[room_id].append(
            websocket
        )

    def disconnect(
        self,
        room_id: str,
        websocket: WebSocket,
    ):
        if room_id in self.rooms:

            if websocket in self.rooms[room_id]:
                self.rooms[room_id].remove(
                    websocket
                )

            if not self.rooms[room_id]:
                del self.rooms[room_id]

    async def send_personal(
        self,
        websocket: WebSocket,
        message,
    ):
        await websocket.send_json(message)

    async def broadcast(
        self,
        room_id: str,
        message,
    ):
        if room_id not in self.rooms:
            return

        dead = []

        for connection in self.rooms[room_id]:

            try:
                await connection.send_json(
                    message
                )

            except Exception:
                dead.append(connection)

        for connection in dead:
            self.disconnect(
                room_id,
                connection,
            )


manager = ConnectionManager()