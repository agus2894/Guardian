# routers/scan.py
from fastapi import APIRouter, Query
import subprocess
from db.devices import save_device
from db.whitelist import is_ip_authorized
from db.alerts import create_alert

router = APIRouter(prefix="/scan", tags=["Escaneo"])

def scan_network(network_range):
    result = subprocess.run(
        ["nmap", "-sn", network_range],
        capture_output=True, text=True
    )
    devices = []
    lines = result.stdout.split("\n")
    for line in lines:
        if "Nmap scan report for" in line:
            ip = line.split(" ")[-1].strip()
            devices.append({
                "ip": ip,
                "authorized": is_ip_authorized(ip)
            })
    return devices

@router.get("/")
async def scan(network_range: str = Query("192.168.0.0/24")):
    dispositivos = scan_network(network_range)
    alertas_generadas = []

    for d in dispositivos:
        ip = d["ip"]
        autorizado = d["authorized"]

        save_device(ip, mac="")

        if not autorizado:
            desc = f"Dispositivo NO autorizado detectado - IP: {ip}"
            create_alert("Intrusión", desc)
            alertas_generadas.append(desc)

    return {
        "dispositivos_detectados": dispositivos,
        "alertas_generadas": alertas_generadas
    }
