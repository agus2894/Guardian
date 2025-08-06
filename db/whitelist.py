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
    cursor.execute("SELECT id, name, ip FROM whitelist")
    results = cursor.fetchall()
    conn.close()
    return [{"id": row[0], "name": row[1], "ip": row[2]} for row in results]

def add_to_whitelist(name, ip):
    conn = sqlite3.connect("guardian.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO whitelist (name, ip) VALUES (?, ?)",
        (name, ip)
    )
    conn.commit()
    conn.close()
