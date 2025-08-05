import sqlite3
from datetime import datetime

def create_alert(alert_type, description):
    conn = sqlite3.connect("guardian.db")
    cursor = conn.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO alerts (type, timestamp, description) VALUES (?, ?, ?)",
        (alert_type, timestamp, description)
    )

    conn.commit()
    conn.close()

def clear_alerts():
    conn = sqlite3.connect("guardian.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM alerts")
    conn.commit()
    conn.close()

def get_all_alerts():
    conn = sqlite3.connect("guardian.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, type, timestamp, description FROM alerts ORDER BY timestamp DESC")
    results = cursor.fetchall()
    conn.close()

    return [
        {"id": row[0], "type": row[1], "timestamp": row[2], "description": row[3]}
        for row in results
    ]
