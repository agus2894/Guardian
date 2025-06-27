import sqlite3

DB_NAME = "guardian.db"

def is_mac_authorized(mac):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM whitelist WHERE mac = ?", (mac,))
    result = cursor.fetchone()

    conn.close()
    return result is not None
