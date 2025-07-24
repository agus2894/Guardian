from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from routers import scan, alerts, whitelist
from db.database import init_db
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Guardián - Sistema de Monitoreo de Red")

# Middleware para sesión
app.add_middleware(SessionMiddleware, secret_key="clave_super_secreta")

# Inicializar DB
init_db()

# Archivos estáticos y plantillas
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Rutas de la API
app.include_router(scan.router)
app.include_router(alerts.router)
app.include_router(whitelist.router)

# Redirección raíz
@app.get("/")
async def root():
    return RedirectResponse(url="/dashboard")

# Mostrar login
@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Validar login
@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    valid_user = os.getenv("LOGIN_USER")
    valid_pass = os.getenv("LOGIN_PASSWORD")

    if username == valid_user and password == valid_pass:
        request.session["logged_in"] = True
        return RedirectResponse(url="/dashboard", status_code=302)
    else:
        return HTMLResponse(content="Usuario o contraseña incorrectos", status_code=401)

# Logout
@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login")

# Dashboard (protegido)
@app.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard(request: Request):
    if not request.session.get("logged_in"):
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("index.html", {"request": request})
