from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os

from db.database import init_db
from routers import scan, alerts, whitelist, devices

# Cargar variables de entorno
load_dotenv()

# Crear app
app = FastAPI(title="Guardián - Sistema de Monitoreo de Red")

# Inicializar la base de datos
init_db()

# Cargar archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Plantillas HTML
templates = Jinja2Templates(directory="templates")

# Incluir rutas de API
app.include_router(scan.router)
app.include_router(alerts.router)
app.include_router(whitelist.router)
app.include_router(devices.router)

# Redirigir raíz a /dashboard
@app.get("/")
async def root():
    return RedirectResponse(url="/dashboard")

# Página del dashboard
@app.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Login básico
@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    valid_user = os.getenv("GUARDIAN_USER")
    valid_pass = os.getenv("GUARDIAN_PASS")

    if username == valid_user and password == valid_pass:
        return RedirectResponse(url="/dashboard", status_code=302)
    else:
        return HTMLResponse(content="Usuario o contraseña incorrectos", status_code=401)
