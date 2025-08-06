from fastapi import FastAPI, Request, Form, Response, Cookie
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os

from db.database import init_db
from routers import scan, alerts, whitelist, devices

load_dotenv()
app = FastAPI(title="Guardián - Sistema de Monitoreo de Red")

# DB + archivos estáticos y plantillas
init_db()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Incluir routers
app.include_router(scan.router)
app.include_router(alerts.router)
app.include_router(whitelist.router)
app.include_router(devices.router)

# Inicio → Login
@app.get("/")
async def root():
    return RedirectResponse(url="/login")

# Mostrar login
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
        response.set_cookie(key="logged_in", value="yes", httponly=True)
        return response
    else:
        return HTMLResponse("Usuario o contraseña incorrectos", status_code=401)

# Cerrar sesión
@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("logged_in")
    return response

# Dashboard protegido
@app.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard(request: Request, logged_in: str = Cookie(default=None)):
    if logged_in != "yes":
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("index.html", {"request": request})
