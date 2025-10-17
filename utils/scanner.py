"""
Este módulo implementa técnicas de escaneo de red enseñadas por el profesor.
Más eficiente que nmap sin permisos de root
Gracias Profe 
"""

import nmap
import subprocess
import re
import platform
import ipaddress
import netifaces
from utils.simple_logger import simple_logger, simple_metrics
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import time

def get_default_cidr():
    try:
        gws = netifaces.gateways()
        default = gws.get('default', {}).get(netifaces.AF_INET)
        if not default:
            simple_logger.warning("No se pudo detectar puerta de enlace por defecto")
            return "192.168.1.0/24"
        
        iface = default[1]
        addrs = netifaces.ifaddresses(iface).get(netifaces.AF_INET)
        if not addrs:
            simple_logger.warning(f"No se encontraron direcciones en la interfaz {iface}")
            return "192.168.1.0/24"  # Fallback común
            
        addr = addrs[0]
        ip = addr['addr']
        netmask = addr['netmask']
        
        # Calcular red
        ip_int = int(ipaddress.IPv4Address(ip))
        mask_int = int(ipaddress.IPv4Address(netmask))
        network_int = ip_int & mask_int
        network = ipaddress.IPv4Address(network_int)
        
        # Convertir mask a prefixlen
        prefixlen = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False).prefixlen
        cidr = f"{network}/{prefixlen}"
        
        simple_logger.info(f"Auto-detected network: {cidr} on interface {iface}")
        return cidr
        
    except Exception as e:
        simple_logger.warning(f"Error detecting network: {str(e)}, using fallback")
        return "192.168.1.0/24"

def scan_network(rango):
    start_time = datetime.now()
    simple_logger.network(f"Starting network scan on {rango}")

    try:
        simple_logger.info(f"Using ping+arp method (professor's approach) for {rango}")
        activos = scan_with_ping_then_arp(rango)
        method_used = "ping+arp"
        
        if not activos:
            simple_logger.warning("Ping+ARP found no devices, trying nmap as fallback")
            activos = scan_with_nmap(rango)
            method_used = "nmap_fallback"
            
    except Exception as e:
        simple_logger.error(f"Ping+ARP scan failed: {str(e)}, trying nmap fallback", network_range=rango)
        try:
            activos = scan_with_nmap(rango)
            method_used = "nmap_fallback"
        except Exception as e2:
            simple_logger.error(f"All scan methods failed: {str(e2)}", network_range=rango)
            simple_metrics.record("network", "scan_error", error=str(e2))
            return []

    end_time = datetime.now()
    scan_duration = (end_time - start_time).total_seconds()

    simple_logger.network(
        f"Scan completed on {rango} using {method_used}",
        devices_found=len(activos),
        duration_seconds=scan_duration
    )

    simple_metrics.record("network", "scan_completed",
                         devices_found=len(activos),
                         duration=scan_duration,
                         network_range=rango,
                         method=method_used)

    return activos

def scan_with_nmap(network_cidr):
    try:
        import nmap
    except ImportError:
        raise RuntimeError("python-nmap no instalado.")
    
    nm = nmap.PortScanner()
    nm.scan(hosts=network_cidr, arguments='-sn')
    hosts = []
    
    for host in nm.all_hosts():
        addr = nm[host].get('addresses', {})
        ip = addr.get('ipv4') or addr.get('ipv6') or host
        mac = addr.get('mac')
        hostname = nm[host].get('hostnames', [{}])[0].get('name') or "Desconocido"
        
        if not mac or mac == "":
            simple_logger.info(f"nmap no obtuvo MAC para {ip}, usando método alternativo")
            mac = get_mac_from_arp(ip)
        
        hosts.append({
            'ip': ip, 
            'mac': mac or "Desconocida", 
            'hostname': hostname
        })
    
    return hosts

def get_mac_from_arp(ip):
    """Obtiene MAC de la tabla ARP del sistema"""
    try:
        # Primero hacer ping para asegurar que esté en tabla ARP
        subprocess.run(['ping', '-c', '1', '-W', '1', ip], 
                      capture_output=True, timeout=2)
        
        try:
            with open("/proc/net/arp") as f:
                lines = f.readlines()[1:]
            
            for line in lines:
                parts = line.split()
                if len(parts) >= 4 and parts[0] == ip:
                    mac = parts[3]
                    if mac != "00:00:00:00:00:00" and mac != "<incomplete>":
                        return mac
                        
        except FileNotFoundError:
            try:
                result = subprocess.run(['arp', '-n', ip], 
                                      capture_output=True, text=True, timeout=2)
                if result.returncode == 0:
                    match = re.search(r'([0-9a-f]{2}[:-][0-9a-f]{2}[:-][0-9a-f]{2}[:-][0-9a-f]{2}[:-][0-9a-f]{2}[:-][0-9a-f]{2})', 
                                    result.stdout, re.IGNORECASE)
                    if match:
                        return match.group(1)
            except Exception:
                pass
                
        return None
        
    except Exception as e:
        simple_logger.info(f"Error getting MAC for {ip}: {str(e)}")
        return None

def scan_with_ping_then_arp(network_cidr):
    simple_logger.info(f"Starting ping+arp scan for {network_cidr}")
    
    try:
        net = ipaddress.ip_network(network_cidr, strict=False)
        ips = [str(ip) for ip in net.hosts()]
        
        simple_logger.info(f"Pinging {len(ips)} hosts in parallel...")
        
        with ThreadPoolExecutor(max_workers=200) as executor:
            executor.map(_ping, ips)
        
        time.sleep(1)
        
        simple_logger.info("Reading ARP table...")
        results = parse_proc_arp()
        
        simple_logger.info(f"Ping+ARP scan found {len(results)} active devices")
        return results
        
    except Exception as e:
        simple_logger.error(f"Ping+ARP scan error: {str(e)}")
        return []

def _ping(host):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    try:
        subprocess.run(['ping', param, '1', host], 
                      stdout=subprocess.DEVNULL, 
                      stderr=subprocess.DEVNULL, 
                      timeout=1)
    except Exception:
        pass

def parse_proc_arp():
    results = []
    try:
        with open("/proc/net/arp") as f:
            lines = f.readlines()[1:]
        
        for line in lines:
            parts = line.split()
            if len(parts) >= 4:
                ip = parts[0]
                mac = parts[3]
                if mac != "00:00:00:00:00:00" and mac != "<incomplete>":
                    results.append({
                        'ip': ip, 
                        'mac': mac, 
                        'hostname': None
                    })
                    
    except FileNotFoundError:
        try:
            out = subprocess.check_output(["arp", "-a"], text=True)
            entries = []
            for line in out.splitlines():
                match = re.search(r'\(?([\d\.]+)\)?\s+.*?([0-9a-f]{2}[:-][0-9a-f]{2}[:-][0-9a-f]{2}[:-][0-9a-f]{2}[:-][0-9a-f]{2}[:-][0-9a-f]{2})', line, re.IGNORECASE)
                if match:
                    ip, mac = match.group(1), match.group(2)
                    entries.append({
                        'ip': ip, 
                        'mac': mac, 
                        'hostname': None
                    })
            results = entries
        except Exception as e:
            simple_logger.warning(f"Could not parse ARP table on Windows/macOS: {str(e)}")
    
    simple_logger.info(f"ARP table parsed: {len(results)} entries found")
    return results

def get_mac_address(ip):
    try:
        subprocess.run(['ping', '-c', '1', ip],
                      capture_output=True, timeout=2)

        result = subprocess.run(['arp', '-n', ip],
                               capture_output=True, text=True)

        if result.returncode == 0:
            mac_pattern = r'([0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}'
            match = re.search(mac_pattern, result.stdout)
            if match:
                return match.group()

        return "Desconocida"
    except Exception as e:
        simple_logger.warning(f"MAC resolution error for IP {ip}: {str(e)}")
        return "Desconocida"
