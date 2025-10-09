from fastapi import APIRouter, Query, Depends
from fastapi.responses import JSONResponse
from utils.auth import get_current_user
from db.devices import get_all_devices
from db.database import get_db_connection
from datetime import datetime, timedelta

router = APIRouter(prefix="/devices", tags=["Dispositivos"])

@router.get("/")
async def get_devices():
    return get_all_devices()

@router.get("/detailed")
async def get_devices_detailed(
    hours: int = Query(24, ge=1, le=168),
    current_user: str = Depends(get_current_user)
):
    """Obtener información detallada de dispositivos"""
    try:
        since_time = (datetime.now() - timedelta(hours=hours)).isoformat()
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Obtener dispositivos únicos con su información más reciente
            cursor.execute('''
                SELECT 
                    d.ip,
                    d.mac,
                    d.last_seen,
                    COUNT(*) as detections,
                    CASE WHEN w.id IS NOT NULL THEN 1 ELSE 0 END as authorized,
                    w.name as whitelist_name
                FROM devices d
                LEFT JOIN whitelist w ON (d.ip = w.ip OR d.mac = w.mac)
                WHERE d.last_seen > ?
                GROUP BY d.ip, d.mac
                ORDER BY d.last_seen DESC
            ''', (since_time,))
            
            devices = cursor.fetchall()
            
            # Obtener estadísticas básicas
            cursor.execute('''
                SELECT 
                    COUNT(DISTINCT ip) as unique_ips,
                    COUNT(DISTINCT mac) as unique_macs
                FROM devices 
                WHERE last_seen > ?
            ''', (since_time,))
            
            stats = cursor.fetchone()
        
        device_list = [
            {
                "ip": device[0],
                "mac": device[1] if device[1] else "No disponible",
                "last_seen": device[2],
                "detections": device[3],
                "authorized": bool(device[4]),
                "whitelist_name": device[5] if device[5] else None
            }
            for device in devices
        ]

        return JSONResponse(content={
            "devices": device_list,
            "statistics": {
                "unique_ips": stats[0] if stats[0] else 0,
                "unique_macs": stats[1] if stats[1] else 0,
                "time_range_hours": hours
            }
        })
        
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)