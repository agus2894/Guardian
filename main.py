from fastapi import FastAPI, Request, Form, Response, Cookie
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routers import scan, alerts, whitelist
from db.database import init_db
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Guardián - Sistema de Monitoreo de Red")

# Inicializar base de datos
init_db()

# Archivos estáticos y plantillas
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Rutas de API
app.include_router(scan.router)
app.include_router(alerts.router)
app.include_router(whitelist.router)

# Ruta raíz redirige a /login
@app.get("/")
async def root():
    return RedirectResponse(url="/login")

# Formulario de login
@app.get("/login", response_class=HTMLResponse)
async def show_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Procesar login
@app.post("/login")
async def login(response: Response, username: str = Form(...), password: str = Form(...)):
    valid_user = os.getenv("GUARDIAN_USER")
    valid_pass = os.getenv("GUARDIAN_PASS")

    if username == valid_user and password == valid_pass:
        response = RedirectResponse(url="/dashboard", status_code=302)
        response.set_cookie("session", "ok")
        return response
    else:
        return HTMLResponse(content="Usuario o contraseña incorrectos", status_code=401)

# Cerrar sesión
@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login")
    response.delete_cookie("session")
    return response

# Dashboard protegido
@app.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard(request: Request, session: str = Cookie(default=None)):
    if session != "ok":
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("index.html", {"request": request})
