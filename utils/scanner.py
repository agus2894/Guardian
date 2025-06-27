import nmap

def scan_network(network_range="192.168.0.0/24"):
    nm = nmap.PortScanner()
    # -sn = ping scan, necesita permisos de raw socket
    nm.scan(hosts=network_range, arguments="-sn")

    devices = []
    for host in nm.all_hosts():
        ip = nm[host]['addresses'].get('ipv4', '')
        mac = nm[host]['addresses'].get('mac', '')  # cadena vacía si no hay MAC
        devices.append({"ip": ip, "mac": mac})
    return devices
