# routers/alerts.py

from fastapi import APIRouter, Depends
from utils.auth import get_current_user
from db.database import get_db_connection

router = APIRouter(prefix="/alerts", tags=["Alertas"])

@router.get("/")
async def get_alerts(current_user: str = Depends(get_current_user)):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, type, timestamp, description FROM alerts ORDER BY timestamp DESC")
        results = cursor.fetchall()

    return [
        {"id": row[0], "type": row[1], "timestamp": row[2], "description": row[3]}
        for row in results
    ]

@router.delete("/clear")
async def clear_alerts(current_user: str = Depends(get_current_user)):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM alerts")
        conn.commit()
    return {"mensaje": "Alertas eliminadas"}
