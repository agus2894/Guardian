from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from routers import scan, alerts, whitelist
from db.database import init_db
from utils.auth import check_login, login_user

app = FastAPI(title="Guardián - Sistema de Monitoreo de Red")
templates = Jinja2Templates(directory="templates")

# Rutas principales
app.include_router(scan.router)
app.include_router(alerts.router)
app.include_router(whitelist.router)

init_db()

@app.get("/")
async def root():
    return RedirectResponse(url="/login")

@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if login_user(username, password):
        response = RedirectResponse(url="/dashboard", status_code=302)
        response.set_cookie(key="session", value="active")
        return response
    return templates.TemplateResponse("login.html", {"request": request, "error": "Credenciales incorrectas"})

@app.get("/dashboard")
async def dashboard(request: Request):
    check_login(request)
    return FileResponse("static/index.html")
