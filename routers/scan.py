# routers/scan.py
from fastapi import APIRouter, Query
import subprocess
from db.devices import save_device
from db.whitelist import is_ip_authorized
from db.alerts import create_alert

router = APIRouter(prefix="/scan", tags=["Escaneo"])

def limpiar_ip(ip_str: str) -> str:
    """Limpia el string de IP quitando paréntesis, hostnames y espacios."""
    ip_str = ip_str.strip()
    # Si viene como "hostname (IP)" nos quedamos solo con la IP
    if "(" in ip_str and ")" in ip_str:
        ip_str = ip_str.split("(")[-1].split(")")[0]
    return ip_str

def scan_network(network_range):
    result = subprocess.run(
        ["nmap", "-sn", network_range],
        capture_output=True, text=True
    )
    devices = []
    lines = result.stdout.split("\n")
    for line in lines:
        if "Nmap scan report for" in line:
            raw_ip = line.split(" ")[-1].strip()
            ip = limpiar_ip(raw_ip)  # limpiamos bien la IP
            devices.append({
                "ip": ip,
                "authorized": is_ip_authorized(ip.strip())  # comparamos limpio
            })
    return devices

@router.get("/")
async def scan(network_range: str = Query("192.168.0.0/24")):
    dispositivos = scan_network(network_range)
    alertas_generadas = []

    for d in dispositivos:
        ip = d["ip"]
        autorizado = d["authorized"]

        save_device(ip, mac="")  # aún sin MAC

        if not autorizado:
            desc = f"Dispositivo NO autorizado detectado - IP: {ip}"
            create_alert("Intrusión", desc)
            alertas_generadas.append(desc)

    return {
        "dispositivos_detectados": dispositivos,
        "alertas_generadas": alertas_generadas
    }
