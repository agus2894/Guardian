from fastapi import APIRouter
from db.devices import get_all_devices

router = APIRouter(prefix="/devices", tags=["Dispositivos"])

@router.get("/")
async def get_devices():
    return get_all_devices()
