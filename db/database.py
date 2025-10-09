import sqlite3
from contextlib import contextmanager

DATABASE_PATH = "guardian.db"

@contextmanager
def get_db_connection():
    """Context manager para conexiones de base de datos"""
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_db_connection() as conn:
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
