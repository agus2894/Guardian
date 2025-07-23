from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse
from routers import scan, alerts, whitelist
from db.database import init_db
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Guardián - Sistema de Monitoreo de Red")

# Inicializar base de datos
init_db()

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Plantillas HTML
templates = Jinja2Templates(directory="templates")

# Rutas de la API
app.include_router(scan.router)
app.include_router(alerts.router)
app.include_router(whitelist.router)

# Redirigir raíz a /docs
@app.get("/")
async def root():
    return RedirectResponse(url="/dashboard")

# Página del Dashboard HTML
@app.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Login (formulario sencillo para el dashboard, si se activa)
@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    valid_user = os.getenv("LOGIN_USER")
    valid_pass = os.getenv("LOGIN_PASSWORD")
    
    if username == valid_user and password == valid_pass:
        return RedirectResponse(url="/dashboard", status_code=302)
    else:
        return HTMLResponse(content="Usuario o contraseña incorrectos", status_code=401)
