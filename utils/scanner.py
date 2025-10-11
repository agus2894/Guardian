"""
MÓDULO DE ESCÁNER DE RED - DETECCIÓN DE DISPOSITIVOS
===================================================

CONCEPTOS DE CIBERSEGURIDAD:

1. RECONOCIMIENTO DE RED:
   - Descubrimiento de dispositivos activos en la red
   - Identificación de direcciones MAC para fingerprinting
   - Mapeo de la topología de red

2. DETECCIÓN DE INTRUSIONES:
   - Comparación con whitelist de dispositivos autorizados
   - Identificación de dispositivos sospechosos o no autorizados
   - Alertas automáticas ante anomalías

3. TÉCNICAS UTILIZADAS:
   - Ping sweep: Verificar hosts activos sin abrir puertos
   - ARP scanning: Obtener direcciones MAC de la capa 2
   - Nmap: Herramienta profesional de reconocimiento

4. LOGGING DE SEGURIDAD:
   - Registro de todos los escaneos para auditoría
   - Métricas de rendimiento y efectividad
   - Trazabilidad para investigación forense
"""

import nmap
import subprocess
import re
from utils.simple_logger import simple_logger, simple_metrics
from datetime import datetime

def scan_network(rango):
    """
    FUNCIÓN PRINCIPAL DE ESCANEO DE RED
    
    Parámetros:
        rango: Rango de IPs a escanear (ej: "192.168.1.0/24")
    
    Proceso:
        1. Inicia escaneo con nmap usando técnica ping (-sn)
        2. Identifica hosts activos sin escanear puertos
        3. Obtiene direcciones MAC de cada host
        4. Registra resultados en logs de seguridad
    """
    start_time = datetime.now()
    simple_logger.network(f"Starting network scan on {rango}")
    
    # INICIALIZAR SCANNER NMAP
    nm = nmap.PortScanner()
    try:
        # ESCANEO PING SWEEP - Detecta hosts activos sin ser intrusivo
        nm.scan(hosts=rango, arguments="-sn")
    except Exception as e:
        simple_logger.error(f"Network scan error: {str(e)}", network_range=rango)
        simple_metrics.record("network", "scan_error", error=str(e))
        return []

    # PROCESAR RESULTADOS DEL ESCANEO
    activos = []
    for host in nm.all_hosts():
        # Obtener dirección MAC para identificación única
        mac = get_mac_address(host)
        activos.append({
            "ip": host,
            "mac": mac
        })
    
    # MÉTRICAS DE RENDIMIENTO
    end_time = datetime.now()
    scan_duration = (end_time - start_time).total_seconds()
    
    # LOGGING COMPLETO PARA AUDITORÍA
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
