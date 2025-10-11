"""
MÓDULO DE GESTIÓN DE ALERTAS DE SEGURIDAD
=========================================

CONCEPTOS DE CIBERSEGURIDAD:

1. SISTEMA DE ALERTAS:
   - Detección y notificación automática de eventos de seguridad
   - Clasificación por tipo y severidad
   - Registro persistente para análisis forense

2. DETECCIÓN DE INTRUSIONES:
   - Identificación de dispositivos no autorizados
   - Extracción de información relevante (IP, MAC)
   - Correlación con whitelist de dispositivos

3. RESPUESTA A INCIDENTES:
   - Notificaciones inmediatas por email
   - Logging estructurado para investigación
   - Métricas para análisis de tendencias

4. CUMPLIMIENTO Y AUDITORÍA:
   - Trazabilidad completa de eventos
   - Timestamps precisos para línea de tiempo
   - Información contextual para cada alerta
"""

from datetime import datetime
from utils.mailer import send_intrusion_alert_sync
from utils.simple_logger import simple_logger, simple_metrics
from db.database import get_db_connection
import os

def create_alert(alert_type, description, send_email=True):
    """
    CREACIÓN DE ALERTA DE SEGURIDAD
    
    Parámetros:
        alert_type: Tipo de alerta (intrusión, advertencia, información)
        description: Descripción detallada del evento
        send_email: Si enviar notificación por email
    
    Proceso:
        1. Almacena alerta en base de datos con timestamp
        2. Registra en logs de seguridad según severidad
        3. Envía notificación por email si es crítica
        4. Actualiza métricas del sistema
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # ALMACENAR ALERTA EN BASE DE DATOS
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO alerts (type, timestamp, description) VALUES (?, ?, ?)",
            (alert_type, timestamp, description)
        )
        conn.commit()
    
    # PROCESAMIENTO ESPECIAL PARA ALERTAS DE INTRUSIÓN
    if alert_type.lower() == "intrusión":
        # EXTRACCIÓN DE INFORMACIÓN CRÍTICA
        ip = mac = "Desconocida"
        
        if "IP:" in description:
            ip = description.split("IP:")[1].split(",")[0].strip()
        
        if "MAC:" in description:
            mac = description.split("MAC:")[1].strip()
        
        simple_logger.security(
            description,
            severity="high",
            event_type="intrusion_detected",
            ip=ip,
            mac=mac
        )
        
        simple_metrics.record("security", "intrusion_alert", ip=ip, mac=mac)
        
        # Enviar notificación por email si está habilitada
        if send_email and os.getenv("EMAIL_NOTIFICATIONS", "false").lower() == "true":
            try:
                send_intrusion_alert_sync(ip, mac)
                simple_logger.info("Email notification sent successfully", ip=ip, mac=mac)
                simple_metrics.record("notifications", "email_sent", ip=ip)
            except Exception as e:
                simple_logger.error(f"Email notification error: {str(e)}", ip=ip, mac=mac)
                simple_metrics.record("notifications", "email_error", error=str(e))
    else:
        simple_logger.info(f"Alert created: {alert_type} - {description}", alert_type=alert_type)
        simple_metrics.record("security", "general_alert", alert_type=alert_type)

def clear_alerts():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Contar alertas antes de eliminar
        cursor.execute("SELECT COUNT(*) FROM alerts")
        count = cursor.fetchone()[0]
        
        cursor.execute("DELETE FROM alerts")
        conn.commit()
    
    simple_logger.info(f"Cleared {count} alerts", alerts_count=count)
    simple_metrics.record("admin", "alerts_cleared", count=count)

def get_all_alerts():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, type, timestamp, description FROM alerts ORDER BY timestamp DESC")
        results = cursor.fetchall()

    return [
        {"id": row[0], "alert_type": row[1], "timestamp": row[2], "description": row[3]}
        for row in results
    ]
