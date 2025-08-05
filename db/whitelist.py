import sqlite3

def get_whitelist():
    conn = sqlite3.connect("guardian.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, ip FROM whitelist")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "ip": r[2]} for r in rows]

def add_to_whitelist(name, ip):
    conn = sqlite3.connect("guardian.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO whitelist (name, ip) VALUES (?, ?)", (name, ip))
    conn.commit()
    conn.close()

def is_ip_authorized(ip):
    conn = sqlite3.connect("guardian.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM whitelist WHERE ip = ?", (ip,))
    result = cursor.fetchone()[0]
    conn.close()
    return result > 0
