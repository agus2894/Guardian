from fastapi import APIRouter, Query
from utils.scanner import scan_network
from db.devices import save_device
from db.whitelist import is_ip_authorized
from db.alerts import create_alert

router = APIRouter(prefix="/scan", tags=["Escaneo"])

@router.get("/")
async def scan(network_range: str = Query("192.168.0.0/24")):
    dispositivos = scan_network(network_range)
    alertas_generadas = []

    for d in dispositivos:
        ip = d["ip"]
        save_device(ip, mac="")

        if not is_ip_authorized(ip):
            desc = f"Dispositivo NO autorizado detectado - IP: {ip}"
            create_alert("Intrusión", desc)
            alertas_generadas.append(desc)

    return {
        "dispositivos_detectados": dispositivos,
        "alertas_generadas": alertas_generadas
    }
