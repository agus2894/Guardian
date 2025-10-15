from fastapi import FastAPI
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from routers import scan, alerts, whitelist, scheduler, devices, reports, auth
from db.database import init_db
from utils.simple_scheduler import simple_scheduler
from utils.simple_logger import simple_logger, simple_metrics
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Guardian - Sistema de Monitoreo de Red",
    version="2.0"
)

@app.on_event("startup")
async def startup_event():
    init_db()
    await simple_scheduler.start_scheduler()
    simple_logger.info("Guardian system started")
    simple_metrics.record("system", "startup")

@app.on_event("shutdown")
async def shutdown_event():
    await simple_scheduler.stop_scheduler()
    simple_logger.info("Guardian system shutdown")
    simple_metrics.record("system", "shutdown")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router)
app.include_router(scan.router)
app.include_router(alerts.router)
app.include_router(whitelist.router)
app.include_router(scheduler.router)
app.include_router(devices.router)
app.include_router(reports.router)

@app.get("/")
async def root():
    return RedirectResponse(url="/login")

@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/icons/favicon.ico")
