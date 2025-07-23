import smtplib
from email.message import EmailMessage
import os

EMAIL_ORIGEN = os.getenv("EMAIL_ORIGEN")
EMAIL_CLAVE = os.getenv("EMAIL_CLAVE")
EMAIL_DESTINO = os.getenv("EMAIL_DESTINO")

def enviar_alerta_por_email(ip):
    asunto = "⚠️ Alerta de intrusión en tu red"
    cuerpo = f"Dispositivo NO autorizado detectado:\nIP: {ip}"

    # resto igual...

    mensaje = EmailMessage()
    mensaje["Subject"] = asunto
    mensaje["From"] = EMAIL_ORIGEN
    mensaje["To"] = EMAIL_DESTINO
    mensaje.set_content(cuerpo)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ORIGEN, EMAIL_CLAVE)
            smtp.send_message(mensaje)
        print(f"[EMAIL] Alerta enviada: {ip} - {mac}")
    except Exception as e:
        print(f"[ERROR] Falló el envío de email: {e}")
