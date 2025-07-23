from fastapi import APIRouter
from utils.scanner import scan_network
from db.devices import save_device
from db.whitelist import is_ip_authorized
from db.alerts import create_alert
from utils.mailer import enviar_alerta_por_email

router = APIRouter(prefix="/scan", tags=["Escaneo"])

@router.get("/")
async def scan():
    dispositivos = scan_network("192.168.103.0/24")  # Ajustá el rango según tu red
    alertas_generadas = []

    for d in dispositivos:
        ip = d["ip"]
        save_device(ip, mac="")  # MAC vacía ya que no se usa

        if not is_ip_authorized(ip):
            desc = f"Dispositivo NO autorizado detectado - IP: {ip}"
            create_alert("Intrusión", desc)
            enviar_alerta_por_email(ip)  # solo IP
            alertas_generadas.append(desc)

    return {
        "dispositivos_detectados": dispositivos,
        "alertas_generadas": alertas_generadas
    }
