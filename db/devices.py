import sqlite3
from datetime import datetime

def save_device(ip, mac=""):
    conn = sqlite3.connect("guardian.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO devices (ip, fecha_detectado) VALUES (?, ?)",
        (ip, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    conn.close()

def get_devices():
    conn = sqlite3.connect("guardian.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM devices ORDER BY fecha_detectado DESC")
    dispositivos = cursor.fetchall()
    conn.close()
    return dispositivos
