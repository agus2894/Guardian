"""
MÓDULO DE BASE DE DATOS - PERSISTENCIA DE DATOS DE SEGURIDAD
===========================================================

CONCEPTOS DE CIBERSEGURIDAD:

1. ALMACENAMIENTO SEGURO:
   - Base de datos SQLite local para evitar dependencias externas
   - Transacciones ACID para integridad de datos
   - Context managers para gestión segura de conexiones

2. ESTRUCTURA DE DATOS DE SEGURIDAD:
   - devices: Inventario de dispositivos de red detectados
   - alerts: Registro histórico de eventos de seguridad
   - whitelist: Lista de dispositivos autorizados
   - metrics: Métricas para análisis de rendimiento

3. DISEÑO PARA AUDITORÍA:
   - Timestamps en todos los registros
   - Trazabilidad completa de eventos
   - Información contextual para investigación

4. GESTIÓN DE CONEXIONES:
   - Context managers para prevenir memory leaks
   - Manejo automático de cierre de conexiones
   - Transacciones seguras con rollback automático
"""

import sqlite3
from contextlib import contextmanager

# RUTA DE LA BASE DE DATOS
DATABASE_PATH = "guardian.db"

@contextmanager
def get_db_connection():
    """
    CONTEXT MANAGER PARA CONEXIONES SEGURAS
    
    Beneficios:
        - Cierre automático de conexiones
        - Manejo de excepciones
        - Prevención de memory leaks
        - Transacciones implícitas
    """
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    """
    INICIALIZACIÓN DE ESQUEMA DE BASE DE DATOS
    
    Crea todas las tablas necesarias para el sistema de seguridad:
        - devices: Dispositivos detectados en red
        - alerts: Eventos y alertas de seguridad
        - whitelist: Dispositivos autorizados
        - metrics: Métricas del sistema
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # TABLA DE DISPOSITIVOS DETECTADOS EN RED
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS devices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip TEXT,              -- Dirección IP del dispositivo
                mac TEXT,             -- Dirección MAC (identificador único)
                last_seen TEXT,       -- Timestamp de última detección
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
