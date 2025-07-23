import subprocess
import re

def scan_network(rango_ip):
    resultado = subprocess.run(["nmap", "-sn", rango_ip], capture_output=True, text=True)
    ips = re.findall(r"Nmap scan report for ([\d\.]+)", resultado.stdout)

    dispositivos = []
    for ip in ips:
        dispositivos.append({
            "ip": ip,
            "mac": ""  # No obtenemos MAC
        })

    return dispositivos
