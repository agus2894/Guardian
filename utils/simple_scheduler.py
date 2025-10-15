from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import asyncio
import os
from utils.scanner import scan_network
from db.whitelist import is_device_authorized
from db.alerts import create_alert
from db.devices import save_device
from utils.simple_logger import simple_logger, simple_metrics

class SimpleNetworkScheduler:

    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.is_running = False
        self.scan_count = 0
        self.default_network = os.getenv("DEFAULT_NETWORK_RANGE", "192.168.0.0/24")

    async def start_scheduler(self):
        """Iniciar el scheduler"""
        if not self.scheduler.running:
            self.scheduler.start()
            self.is_running = True
            simple_logger.info("Network scheduler started")
            print("🕒 Scheduler de red iniciado")

    async def stop_scheduler(self):
        """Detener el scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown(wait=False)
            self.is_running = False
            simple_logger.info("Network scheduler stopped")
            print("🛑 Scheduler de red detenido")

    async def add_scheduled_scan(self, interval_minutes: int = 30, network_range: str = None):
        """Agregar escaneo programado (simplificado)"""
        if not network_range:
            network_range = self.default_network

        # Remover job anterior si existe
        try:
            self.scheduler.remove_job('network_scan')
        except:
            pass

        # Agregar nuevo job
        self.scheduler.add_job(
            self._perform_scan,
            'interval',
            minutes=interval_minutes,
            args=[network_range],
            id='network_scan',
            replace_existing=True
        )

        simple_logger.info(f"Scheduled scan configured: every {interval_minutes} minutes on {network_range}")
        simple_metrics.record("scheduler", "scan_scheduled", interval=interval_minutes, network=network_range)

        return True

    async def remove_scheduled_scan(self):
        """Remover escaneo programado"""
        try:
            self.scheduler.remove_job('network_scan')
            simple_logger.info("Scheduled scan removed")
            simple_metrics.record("scheduler", "scan_removed")
            return True
        except:
            return False

    async def _perform_scan(self, network_range: str):
        """Realizar escaneo (método interno simplificado)"""
        try:
            self.scan_count += 1
            simple_logger.network(f"Starting scheduled scan #{self.scan_count}")

            # Ejecutar escaneo
            devices = scan_network(network_range)
            alerts_generated = 0

            for device in devices:
                ip = device["ip"]
                mac = device.get("mac", "")

                # Guardar dispositivo
                save_device(ip, mac)

                # Verificar autorización
                if not is_device_authorized(ip, mac):
                    description = f"Dispositivo NO autorizado detectado - IP: {ip}, MAC: {mac}"
                    create_alert("Intrusión", description)
                    alerts_generated += 1

            simple_logger.network(
                f"Scan #{self.scan_count} completed",
                devices_found=len(devices),
                alerts_generated=alerts_generated,
                network_range=network_range
            )

            simple_metrics.record("network", "scheduled_scan",
                                devices_found=len(devices),
                                alerts_generated=alerts_generated)

        except Exception as e:
            simple_logger.error(f"Scheduled scan failed: {str(e)}", scan_count=self.scan_count)

    def get_status(self):
        """Obtener estado del scheduler (simplificado)"""
        jobs = self.scheduler.get_jobs()
        return {
            "running": self.is_running,
            "scan_count": self.scan_count,
            "active_jobs": len(jobs),
            "next_run": jobs[0].next_run_time.isoformat() if jobs else None
        }

# Instancia global simplificada
simple_scheduler = SimpleNetworkScheduler()
