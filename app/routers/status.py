from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from typing import Dict, Set
from .. import models, schemas
from ..utils import get_current_user  # FIXED import

router = APIRouter(prefix="/status", tags=["Status"])

# In-memory structures (demo only)
DOCTOR_STATUS: Dict[int, str] = {}
SUBSCRIBERS: Dict[int, Set[WebSocket]] = {}

@router.websocket("/ws/doctor/{doctor_id}")
async def ws_doctor_status(websocket: WebSocket, doctor_id: int):
    await websocket.accept()
    SUBSCRIBERS.setdefault(doctor_id, set()).add(websocket)
    # send current status on connect
    await websocket.send_json({"doctor_id": doctor_id, "status": DOCTOR_STATUS.get(doctor_id, "offline")})
    try:
        while True:
            await websocket.receive_text()  # keep alive
    except WebSocketDisconnect:
        SUBSCRIBERS.get(doctor_id, set()).discard(websocket)

@router.post("/doctor/{doctor_id}", response_model=schemas.StatusOut)
def set_doctor_status(
    doctor_id: int,
    payload: schemas.StatusSetRequest,
    current_user: models.User = Depends(get_current_user)
):
    # Ensure only the doctor themself can update
    if current_user.role != "doctor" or current_user.id != doctor_id:
        raise HTTPException(status_code=403, detail="Only the doctor themself can update their status")

    DOCTOR_STATUS[doctor_id] = payload.status

    # Fan-out to WS subscribers
    for ws in list(SUBSCRIBERS.get(doctor_id, set())):
        try:
            # Because we're in sync mode, use loop.create_task
            import asyncio
            asyncio.create_task(ws.send_json({"doctor_id": doctor_id, "status": payload.status}))
        except Exception:
            SUBSCRIBERS[doctor_id].discard(ws)

    return {"doctor_id": doctor_id, "status": payload.status}

@router.get("/doctor/{doctor_id}", response_model=schemas.StatusOut)
def get_doctor_status(doctor_id: int):
    return {"doctor_id": doctor_id, "status": DOCTOR_STATUS.get(doctor_id, "offline")}
