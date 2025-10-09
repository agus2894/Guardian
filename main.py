from fastapi import FastAPI
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from routers import scan, alerts, whitelist, scheduler, devices, reports, auth
from db.database import init_db
from utils.simple_scheduler import simple_scheduler
from utils.simple_logger import simple_logger, simple_metrics
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = FastAPI(title="Guardián - Sistema de Monitoreo de Red")

# Eventos de startup y shutdown
@app.on_event("startup")
async def startup_event():
    """Inicializar servicios al arrancar"""
    init_db()
    await simple_scheduler.start_scheduler()
    simple_logger.info("Guardian system started successfully")
    simple_metrics.record("system", "startup")
    print("🚀 Guardián iniciado correctamente")

@app.on_event("shutdown")
async def shutdown_event():
    """Limpiar recursos al cerrar"""
    await simple_scheduler.stop_scheduler()
    simple_logger.info("Guardian system shutdown")
    simple_metrics.record("system", "shutdown")
    print("🛑 Guardián detenido correctamente")

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Incluir routers
app.include_router(auth.router)
app.include_router(scan.router)
app.include_router(alerts.router)
app.include_router(whitelist.router)
app.include_router(scheduler.router)
app.include_router(devices.router)
app.include_router(reports.router)

# Redirigir raíz a login
@app.get("/")
async def root():
    return RedirectResponse(url="/login")

# Servir favicon
@app.get("/favicon.ico")
async def favicon():
    icon_path = os.path.join("static", "icons", "favicon.ico")
    if os.path.exists(icon_path):
        return FileResponse(icon_path)
    return FileResponse("static/icons/favicon.ico")
