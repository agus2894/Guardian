from fastapi import APIRouter, Request
from utils.scanner import scan_network
from db.devices import save_device
from db.whitelist import is_ip_authorized
from db.alerts import create_alert

router = APIRouter(prefix="/scan", tags=["Escaneo"])

@router.get("/")
async def scan(request: Request):
    dispositivos = scan_network("192.168.0.0/24")  # Podés cambiar el rango si usás tu celu
    alertas_generadas = []

    for d in dispositivos:
        ip = d["ip"]
        save_device(ip)

        if not is_ip_authorized(ip):
            desc = f"Dispositivo NO autorizado detectado - IP: {ip}"
            create_alert("Intrusión", desc)
            alertas_generadas.append(desc)

    return {
        "dispositivos_detectados": dispositivos,
        "alertas_generadas": alertas_generadas
    }
