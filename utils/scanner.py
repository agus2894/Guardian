import nmap

def scan_network(rango):
    nm = nmap.PortScanner()
    try:
        nm.scan(hosts=rango, arguments="-sn")
    except:
        return []

    activos = []
    for host in nm.all_hosts():
        activos.append({"ip": host})
    return activos
