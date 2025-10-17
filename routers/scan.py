from fastapi import APIRouter, Query, Depends
from utils.scanner import scan_network
from utils.auth import get_current_user
from db.devices import save_device
from db.whitelist import is_device_authorized
from db.alerts import create_alert

router = APIRouter(prefix="/scan", tags=["Escaneo"])

@router.get("/")
async def scan(network_range: str = Query("192.168.0.0/24"), current_user: str = Depends(get_current_user)):
    dispositivos = scan_network(network_range)
    alertas_generadas = []

    for d in dispositivos:
        ip = d["ip"]
        mac = d["mac"]
        autorizado = is_device_authorized(ip, mac)

        save_device(ip, mac)

        if not autorizado:
            desc = f"Dispositivo NO autorizado detectado - IP: {ip}, MAC: {mac}"
            create_alert("Intrusión", desc)
            alertas_generadas.append(desc)

        d["authorized"] = autorizado

    return {
        "dispositivos_detectados": dispositivos,
        "alertas_generadas": alertas_generadas
    }
