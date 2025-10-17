from fastapi import APIRouter, Form, Depends, HTTPException
from fastapi.responses import JSONResponse
from utils.auth import get_current_user
from utils.simple_scheduler import simple_scheduler
import os

router = APIRouter(prefix="/scheduler", tags=["Scheduler"])

@router.get("/status")
async def get_scheduler_status(current_user: str = Depends(get_current_user)):

    status = simple_scheduler.get_status()
    return JSONResponse(content=status)

@router.post("/start")
async def start_scheduled_scan(
    interval_minutes: int = Form(30),
    network_range: str = Form(None),
    current_user: str = Depends(get_current_user)
):
    try:
        if interval_minutes < 1 or interval_minutes > 1440:
            raise HTTPException(status_code=400, detail="Intervalo debe ser entre 1 y 1440 minutos")

        if not network_range:
            network_range = os.getenv("DEFAULT_NETWORK_RANGE", "192.168.0.0/24")

        await simple_scheduler.add_scheduled_scan(interval_minutes, network_range)

        return JSONResponse(content={
            "mensaje": f"Escaneo programado iniciado cada {interval_minutes} minutos",
            "network_range": network_range,
            "interval": interval_minutes
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al iniciar scheduler: {str(e)}")

@router.post("/stop")
async def stop_scheduled_scan(current_user: str = Depends(get_current_user)):
    """Detener escaneo programado"""
    try:
        await simple_scheduler.remove_scheduled_scan()
        return JSONResponse(content={"mensaje": "Escaneo programado detenido"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al detener scheduler: {str(e)}")

@router.post("/scan-now")
async def scan_now(
    network_range: str = Form(None),
    current_user: str = Depends(get_current_user)
):
    """Ejecutar escaneo inmediato"""
    try:
        if not network_range:
            network_range = os.getenv("DEFAULT_NETWORK_RANGE", "192.168.0.0/24")

        await simple_scheduler._perform_scan(network_range)
        return JSONResponse(content={"mensaje": "Escaneo ejecutado exitosamente"})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en escaneo: {str(e)}")
