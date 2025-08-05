from fastapi import APIRouter
import sqlite3

router = APIRouter(prefix="/alerts", tags=["Alertas"])

@router.get("/")
async def get_alerts():
    conn = sqlite3.connect("guardian.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, type, timestamp, description FROM alerts ORDER BY timestamp DESC")
    results = cursor.fetchall()
    conn.close()

    return [
        {"id": row[0], "type": row[1], "timestamp": row[2], "description": row[3]}
        for row in results
    ]

@router.delete("/clear")
async def clear_alerts():
    conn = sqlite3.connect("guardian.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM alerts")
    conn.commit()
    conn.close()
    return {"mensaje": "Alertas eliminadas"}
