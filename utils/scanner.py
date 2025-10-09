import nmap
import subprocess
import re
from utils.simple_logger import simple_logger, simple_metrics
from datetime import datetime

def scan_network(rango):
    start_time = datetime.now()
    simple_logger.network(f"Starting network scan on {rango}")
    
    nm = nmap.PortScanner()
    try:
        nm.scan(hosts=rango, arguments="-sn")
    except Exception as e:
        simple_logger.error(f"Network scan error: {str(e)}", network_range=rango)
        simple_metrics.record("network", "scan_error", error=str(e))
        return []

    activos = []
    for host in nm.all_hosts():
        mac = get_mac_address(host)
        activos.append({
            "ip": host,
            "mac": mac
        })
    
    end_time = datetime.now()
    scan_duration = (end_time - start_time).total_seconds()
    
    # Log del resultado
    simple_logger.network(
        f"Scan completed on {rango}",
        devices_found=len(activos),
        duration_seconds=scan_duration
    )
    
    # Métricas
    simple_metrics.record("network", "scan_completed", 
                         devices_found=len(activos),
                         duration=scan_duration,
                         network_range=rango)
    
    return activos

def get_mac_address(ip):
    """Obtiene la MAC address de una IP usando ARP"""
    try:
        # Hacer ping para asegurar que la entrada ARP existe
        subprocess.run(['ping', '-c', '1', ip], 
                      capture_output=True, timeout=2)
        
        # Buscar en la tabla ARP
        result = subprocess.run(['arp', '-n', ip], 
                               capture_output=True, text=True)
        
        if result.returncode == 0:
            # Buscar patrón MAC en la salida
            mac_pattern = r'([0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}'
            match = re.search(mac_pattern, result.stdout)
            if match:
                return match.group()
        
        return "Desconocida"
    except Exception as e:
        simple_logger.warning(f"MAC resolution error for IP {ip}: {str(e)}")
        return "Desconocida"
