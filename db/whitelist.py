import sqlite3

def is_ip_authorized(ip):
    conn = sqlite3.connect("guardian.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM whitelist WHERE ip = ?", (ip,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def get_whitelist():
    conn = sqlite3.connect("guardian.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, ip FROM whitelist")
    results = cursor.fetchall()
    conn.close()
    return [{"name": row[0], "ip": row[1]} for row in results]

def add_to_whitelist(name, ip, mac=None):
    conn = sqlite3.connect("guardian.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO whitelist (name, mac, ip) VALUES (?, ?, ?)",
        (name, mac or "", ip)
    )
    conn.commit()
    conn.close()
