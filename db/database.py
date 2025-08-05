import sqlite3

def init_db():
    conn = sqlite3.connect("guardian.db")
    cursor = conn.cursor()

    # Tabla de dispositivos detectados
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT,
            mac TEXT,
            last_seen TEXT,
            authorized INTEGER DEFAULT 0  -- 1 = autorizado, 0 = no
        )
    ''')

    # Tabla de lista blanca
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS whitelist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            mac TEXT UNIQUE,
            ip TEXT UNIQUE
        )
    ''')

    # Tabla de alertas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            timestamp TEXT,
            description TEXT
        )
    ''')

    conn.commit()
    conn.close()
