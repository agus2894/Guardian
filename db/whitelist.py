import sqlite3

def is_ip_authorized(ip):
    ip = ip.strip()  # Limpia espacios y saltos de línea
    conn = sqlite3.connect("guardian.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM whitelist WHERE TRIM(ip) = ?", (ip,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def get_whitelist():
    conn = sqlite3.connect("guardian.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, ip FROM whitelist")
    results = cursor.fetchall()
    conn.close()
    return [
        {
            "id": row[0],
            "name": row[1].strip() if row[1] else "",
            "ip": row[2].strip()
        }
        for row in results
    ]

def add_to_whitelist(name, ip, mac=None):
    name = name.strip() if name else ""
    ip = ip.strip()
    mac = mac.strip() if mac else ""
    conn = sqlite3.connect("guardian.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO whitelist (name, mac, ip) VALUES (?, ?, ?)",
        (name, mac, ip)
    )
    conn.commit()
    conn.close()
