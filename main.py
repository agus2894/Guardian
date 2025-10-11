"""
GUARDIAN - Sistema de Monitoreo de Red y Seguridad
==================================================

PROPÓSITO EDUCATIVO:
Este sistema demuestra conceptos fundamentales de ciberseguridad:
- Detección de intrusiones en red
- Autenticación y autorización
- Logging de seguridad
- Alertas automáticas
- Reportes de seguridad

ARQUITECTURA:
- FastAPI: Framework web moderno y rápido
- SQLite: Base de datos liviana para almacenamiento
- JWT: Tokens seguros para autenticación
- Nmap: Escáner de red profesional
- Logging estructurado en JSON

FUNCIONALIDADES PRINCIPALES:
1. Escáneo automático de red
2. Detección de dispositivos no autorizados
3. Sistema de alertas en tiempo real
4. Generación de reportes PDF
5. Dashboard web interactivo
"""

from fastapi import FastAPI
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from routers import scan, alerts, whitelist, scheduler, devices, reports, auth
from db.database import init_db
from utils.simple_scheduler import simple_scheduler
from utils.simple_logger import simple_logger, simple_metrics
import os
from dotenv import load_dotenv

# CONFIGURACIÓN INICIAL - Cargar variables de entorno
load_dotenv()

# APLICACIÓN PRINCIPAL FastAPI
app = FastAPI(
    title="Guardian - Sistema de Monitoreo de Red",
    description="Sistema educativo de ciberseguridad para detección de intrusiones",
    version="2.0"
)

# EVENTOS DEL CICLO DE VIDA DE LA APLICACIÓN
@app.on_event("startup")
async def startup_event():
    """
    INICIALIZACIÓN DEL SISTEMA
    - Configura la base de datos SQLite
    - Inicia el scheduler para escaneos automáticos
    - Registra el inicio en logs de seguridad
    """
    init_db()  # Crear tablas si no existen
    await simple_scheduler.start_scheduler()  # Iniciar tareas programadas
    simple_logger.info("Guardian system started successfully")
    simple_metrics.record("system", "startup")
    print("🚀 Guardian iniciado correctamente")

@app.on_event("shutdown")
async def shutdown_event():
    """
    LIMPIEZA AL CERRAR EL SISTEMA
    - Detiene el scheduler
    - Cierra conexiones activas
    - Registra el cierre en logs
    """
    await simple_scheduler.stop_scheduler()
    simple_logger.info("Guardian system shutdown")
    simple_metrics.record("system", "shutdown")
    print("🛑 Guardian detenido correctamente")

# CONFIGURACIÓN DE ARCHIVOS ESTÁTICOS
# Permite servir CSS, JS, imágenes desde la carpeta static/
app.mount("/static", StaticFiles(directory="static"), name="static")

# REGISTRO DE ROUTERS - MÓDULOS FUNCIONALES
# Cada router maneja un aspecto específico del sistema
app.include_router(auth.router)        # Autenticación y autorización
app.include_router(scan.router)        # Escáner de red
app.include_router(alerts.router)      # Sistema de alertas
app.include_router(whitelist.router)   # Gestión de dispositivos autorizados
app.include_router(scheduler.router)   # Tareas programadas
app.include_router(devices.router)     # Gestión de dispositivos
app.include_router(reports.router)     # Generación de reportes

# RUTA PRINCIPAL - Redirige al login para seguridad
@app.get("/")
async def root():
    """Redirigir página principal al sistema de login"""
    return RedirectResponse(url="/login")

# SERVIR FAVICON - Icono del sitio web
@app.get("/favicon.ico")
async def favicon():
    """Servir el favicon del sistema"""
    icon_path = os.path.join("static", "icons", "favicon.ico")
    if os.path.exists(icon_path):
        return FileResponse(icon_path)
    return FileResponse("static/icons/favicon.ico")
