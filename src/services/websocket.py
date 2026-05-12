from fastapi import WebSocket, WebSocketDisconnect


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: dict[int, list[WebSocket]] = {}

    async def connect(self, room_id: int, websocket: WebSocket) -> None:
        await websocket.accept()
        websocket_list = self.active_connections.get(room_id, [])
        websocket_list.append(websocket)
        self.active_connections[room_id] = websocket_list

    def disconnect(self, room_id: int, websocket: WebSocket) -> None:
        websocket_list = self.active_connections.get(room_id)

        if websocket_list is None:
            return

        try:
            websocket_list.remove(websocket)
        except ValueError:
            return

        if not websocket_list:
            del self.active_connections[room_id]

    async def broadcast(self, room_id: int, message: str) -> None:
        for connection in self.active_connections.get(room_id, []):
            await connection.send_text(message)


manager = ConnectionManager()


async def websocket_room_id_service(room_id: int, websocket: WebSocket) -> None:
    await manager.connect(room_id, websocket)

    try:
        while True:
            text = await websocket.receive_text()
            await manager.broadcast(room_id, text)
    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)
