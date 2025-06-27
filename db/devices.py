import sqlite3
from datetime import datetime

DB_NAME = "guardian.db"

def save_device(ip, mac):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    now = datetime.now().isoformat(timespec='seconds')

    cursor.execute("SELECT * FROM devices WHERE mac = ?", (mac,))
    existing = cursor.fetchone()

    if existing:
        # Solo actualizamos la fecha de última detección
        cursor.execute("UPDATE devices SET last_seen = ?, ip = ? WHERE mac = ?", (now, ip, mac))
    else:
        # Insertamos nuevo dispositivo
        cursor.execute("INSERT INTO devices (ip, mac, last_seen) VALUES (?, ?, ?)", (ip, mac, now))

    conn.commit()
    conn.close()

