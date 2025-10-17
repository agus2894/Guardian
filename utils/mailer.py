import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime
import asyncio

async def send_email_notification(subject: str, message: str, to_email: str = None):

    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    from_email = os.getenv("FROM_EMAIL", smtp_username)

    if not to_email:
        to_email = os.getenv("NOTIFICATION_EMAIL")

    if not all([smtp_username, smtp_password, to_email]):
        print("Configuración de email incompleta. Notificación no enviada.")
        return False

    try:
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = f"[Guardián] {subject}"

        # Cuerpo del mensaje con estilo
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; color:
            <div style="background-color:
                <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <h2 style="color:
                        🛡️ Alerta de Seguridad - Guardián
                    </h2>
                    <p style="font-size: 16px; line-height: 1.6;">
                        <strong>Fecha y Hora:</strong> {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
                    </p>
                    <div style="background-color:
                        <p style="margin: 0; font-size: 16px;">
                            <strong>Descripción:</strong><br>
                            {message}
                        </p>
                    </div>
                    <p style="font-size: 14px; color:
                        Este mensaje fue generado automáticamente por el sistema Guardián de monitoreo de red.
                        <br>
                        Por favor, revise su red inmediatamente y tome las medidas necesarias.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """

        msg.attach(MIMEText(html_body, 'html'))

        await aiosmtplib.send(
            msg,
            hostname=smtp_server,
            port=smtp_port,
            start_tls=True,
            username=smtp_username,
            password=smtp_password,
        )

        print(f"Notificación por email enviada a {to_email}")
        return True

    except Exception as e:
        print(f"Error al enviar email: {e}")
        return False

def send_notification_sync(subject: str, message: str, to_email: str = None):
    try:
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(send_email_notification(subject, message, to_email))
    except RuntimeError:
        # Si no hay loop, crear uno nuevo
        return asyncio.run(send_email_notification(subject, message, to_email))

async def send_intrusion_alert(ip: str, mac: str = None):
    """Enviar alerta específica de intrusión"""
    subject = "🚨 INTRUSIÓN DETECTADA"

    if mac and mac != "Desconocida":
        message = f"Se ha detectado un dispositivo no autorizado en su red:\n\nIP: {ip}\nMAC: {mac}\n\nRevise inmediatamente su red y tome las medidas de seguridad necesarias."
    else:
        message = f"Se ha detectado un dispositivo no autorizado en su red:\n\nIP: {ip}\nMAC: No disponible\n\nRevise inmediatamente su red y tome las medidas de seguridad necesarias."

    return await send_email_notification(subject, message)

def send_intrusion_alert_sync(ip: str, mac: str = None):
    """Versión síncrona de la alerta de intrusión"""
    try:
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(send_intrusion_alert(ip, mac))
    except RuntimeError:
        return asyncio.run(send_intrusion_alert(ip, mac))
