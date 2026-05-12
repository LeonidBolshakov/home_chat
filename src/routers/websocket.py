from fastapi import APIRouter, WebSocket

from src.services.websocket import websocket_room_id_service

router = APIRouter(prefix="/wb", tags=["wb"])


@router.websocket("/{room_id}")
async def websocket_room_id_endpoint(room_id: int, websocket: WebSocket):
    await websocket_room_id_service(room_id, websocket)
