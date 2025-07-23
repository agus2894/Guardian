import sqlite3
from datetime import datetime

def create_alert(tipo, descripcion):
    conn = sqlite3.connect("guardian.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO alerts (tipo, descripcion, fecha) VALUES (?, ?, ?)",
        (tipo, descripcion, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    conn.close()

def get_alerts():
    conn = sqlite3.connect("guardian.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alerts ORDER BY fecha DESC")
    alertas = cursor.fetchall()
    conn.close()
    return alertas

def clear_alerts():
    conn = sqlite3.connect("guardian.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM alerts")
    conn.commit()
    conn.close()
