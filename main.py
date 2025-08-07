from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routers import scan, alerts, whitelist
from db.database import init_db
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = FastAPI(title="Guardián - Sistema de Monitoreo de Red")

# Inicializar base de datos
init_db()

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Plantillas HTML
templates = Jinja2Templates(directory="templates")

# Incluir routers
app.include_router(scan.router)
app.include_router(alerts.router)
app.include_router(whitelist.router)

# Redirigir raíz a login
@app.get("/")
async def root():
    return RedirectResponse(url="/login")

# Página de login
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Procesar login
@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    valid_user = os.getenv("GUARDIAN_USER")
    valid_pass = os.getenv("GUARDIAN_PASS")
    
    if username == valid_user and password == valid_pass:
        response = RedirectResponse(url="/dashboard", status_code=302)
        response.set_cookie(key="logged_in", value="true")
        return response
    else:
        return HTMLResponse(content="Usuario o contraseña incorrectos", status_code=401)

# Dashboard protegido por login
@app.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard(request: Request):
    if request.cookies.get("logged_in") != "true":
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("index.html", {"request": request})

# Cerrar sesión
@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie(key="logged_in")
    return response

# Servir favicon (backup en caso de que falle desde static/)
@app.get("/favicon.ico")
async def favicon():
    icon_path = os.path.join("static", "icons", "favicon.ico")
    if os.path.exists(icon_path):
        return FileResponse(icon_path)
    return HTMLResponse(status_code=404, content="Favicon no encontrado")
