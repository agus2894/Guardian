import subprocess
from db.whitelist import is_ip_authorized

def scan_network(network_range):
    result = subprocess.run(
        ["nmap", "-sn", network_range],
        capture_output=True, text=True
    )
    devices = []
    lines = result.stdout.split("\n")
    for line in lines:
        if "Nmap scan report for" in line:
            ip = line.split(" ")[-1].strip()  # Limpieza de IP
            devices.append({
                "ip": ip,
                "authorized": is_ip_authorized(ip)
            })
    return devices
