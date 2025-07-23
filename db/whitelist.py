import sqlite3

def is_ip_authorized(ip):
    conn = sqlite3.connect("guardian.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM whitelist WHERE ip = ?", (ip,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None

def add_to_whitelist(nombre, ip):
    conn = sqlite3.connect("guardian.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO whitelist (nombre, ip) VALUES (?, ?)", (nombre, ip))
    conn.commit()
    conn.close()

def get_whitelist():
    conn = sqlite3.connect("guardian.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM whitelist")
    rows = cursor.fetchall()
    conn.close()
    return rows
