import sqlite3
from datetime import datetime

DB_NAME = "guardian.db"

def create_alert(alert_type, description):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    timestamp = datetime.now().isoformat(timespec='seconds')

    cursor.execute(
        "INSERT INTO alerts (type, timestamp, description) VALUES (?, ?, ?)",
        (alert_type, timestamp, description)
    )

    conn.commit()
    conn.close()
