from datetime import datetime
from utils.mailer import send_intrusion_alert_sync
from utils.simple_logger import simple_logger, simple_metrics
from db.database import get_db_connection
import os

def create_alert(alert_type, description, send_email=True):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO alerts (type, timestamp, description) VALUES (?, ?, ?)",
            (alert_type, timestamp, description)
        )
        conn.commit()

    if alert_type.lower() == "intrusión":
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

        cursor.execute("SELECT COUNT(*) FROM alerts")
        count = cursor.fetchone()[0]

        cursor.execute("DELETE FROM alerts")
        conn.commit()

    simple_logger.info(f"Cleared {count} alerts", alerts_count=count)
    simple_metrics.record("admin", "alerts_cleared", count=count)

def get_all_alerts():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM alerts ORDER BY timestamp DESC")
        return cursor.fetchall()
