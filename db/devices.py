import sqlite3
from datetime import datetime
from db.whitelist import is_ip_authorized

def save_device(ip, mac=""):
    conn = sqlite3.connect("guardian.db")
    cursor = conn.cursor()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    authorized = 1 if is_ip_authorized(ip) else 0

    # Buscar si el dispositivo ya fue registrado
    cursor.execute("SELECT id FROM devices WHERE ip = ?", (ip,))
    result = cursor.fetchone()

    if result:
        cursor.execute(
            "UPDATE devices SET last_seen = ?, authorized = ? WHERE id = ?",
            (now, authorized, result[0])
        )
    else:
        cursor.execute(
            "INSERT INTO devices (ip, mac, last_seen, authorized) VALUES (?, ?, ?, ?)",
            (ip, mac, now, authorized)
        )

    conn.commit()
    conn.close()

def get_all_devices():
    conn = sqlite3.connect("guardian.db")
    cursor = conn.cursor()

    cursor.execute("SELECT ip, mac, last_seen, authorized FROM devices ORDER BY last_seen DESC")
    devices = cursor.fetchall()
    conn.close()

    return [
        {"ip": row[0], "mac": row[1], "last_seen": row[2], "authorized": bool(row[3])}
        for row in devices
    ]
