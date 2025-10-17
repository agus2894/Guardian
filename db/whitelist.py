from db.database import get_db_connection

def is_device_authorized(ip, mac=None):

    ip = ip.strip() if ip else ""
    mac = mac.strip() if mac else ""

    with get_db_connection() as conn:
        cursor = conn.cursor()

        if mac and mac != "Desconocida":
            cursor.execute("SELECT id FROM whitelist WHERE TRIM(ip) = ? OR TRIM(mac) = ?", (ip, mac))
        else:
            cursor.execute("SELECT id FROM whitelist WHERE TRIM(ip) = ?", (ip,))

        result = cursor.fetchone()
    return result is not None

def is_ip_authorized(ip):
    return is_device_authorized(ip)

def get_whitelist():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, ip, mac FROM whitelist")
        results = cursor.fetchall()

    return [
        {
            "id": row[0],
            "name": row[1].strip() if row[1] else "",
            "ip": row[2].strip() if row[2] else "",
            "mac": row[3].strip() if row[3] else ""
        }
        for row in results
    ]

def add_to_whitelist(name, ip, mac=None):
    name = name.strip() if name else ""
    ip = ip.strip() if ip else ""
    mac = mac.strip() if mac else ""

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO whitelist (name, mac, ip) VALUES (?, ?, ?)",
            (name, mac, ip)
        )
        conn.commit()

def get_whitelist_entries():
    """Alias para mantener compatibilidad"""
    return get_whitelist()
