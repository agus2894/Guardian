from fastapi import APIRouter, Query
from utils.scanner import scan_network
from db.devices import save_device
from db.whitelist import is_mac_authorized
from db.alerts import create_alert
from utils.mailer import enviar_alerta_por_email

router = APIRouter(prefix="/scan", tags=["Escaneo"])

@router.get("/")
async def scan(network_range: str = Query("192.168.0.0/24", description="Rango de red a escanear")):
    dispositivos = scan_network(network_range)
    alertas_generadas = []

    for d in dispositivos:
        ip, mac = d["ip"], d["mac"]
        save_device(ip, mac)

        if mac:
            if not is_mac_authorized(mac):
                desc = f"Dispositivo no autorizado detectado - IP: {ip}, MAC: {mac}"
                create_alert("Intrusión", desc)
                alertas_generadas.append(desc)
                enviar_alerta_por_email(ip, mac)

    return {
        "dispositivos_detectados": dispositivos,
        "alertas_generadas": alertas_generadas
    }
