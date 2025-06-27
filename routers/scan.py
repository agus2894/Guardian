from fastapi import APIRouter
from utils.scanner import scan_network
from db.devices import save_device
from db.whitelist import is_mac_authorized
from db.alerts import create_alert

router = APIRouter(prefix="/scan", tags=["Escaneo"])

@router.get("/")
async def scan():
    dispositivos = scan_network("192.168.0.0/24")  # Ajusta el rango si tu red es distinta
    alertas_generadas = []

    for d in dispositivos:
        ip, mac = d["ip"], d["mac"]
        save_device(ip, mac)

        # Solo procesamos alertas si tenemos MAC
        if mac:
            if not is_mac_authorized(mac):
                desc = f"Dispositivo no autorizado detectado - IP: {ip}, MAC: {mac}"
                create_alert("Intrusión", desc)
                alertas_generadas.append(desc)

    return {
        "dispositivos_detectados": dispositivos,
        "alertas_generadas": alertas_generadas
    }
