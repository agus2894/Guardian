from fastapi import APIRouter
import sqlite3

router = APIRouter(prefix="/whitelist", tags=["Whitelist"])

@router.post("/add")
async def add_to_whitelist(data: dict):
    name = data.get("name")
    mac = data.get("mac")
    ip = data.get("ip")

    conn = sqlite3.connect("guardian.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO whitelist (name, mac, ip) VALUES (?, ?, ?)", (name, mac, ip))
    conn.commit()
    conn.close()

    return {"message": "Dispositivo agregado a la whitelist"}
