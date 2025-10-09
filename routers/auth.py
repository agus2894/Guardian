# routers/auth.py

from fastapi import APIRouter, Request, Form, HTTPException, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from utils.auth import authenticate_user, create_access_token, get_current_user, generate_csrf_token
from utils.simple_logger import simple_logger, simple_metrics
from datetime import timedelta

router = APIRouter(tags=["Autenticación"])
templates = Jinja2Templates(directory="templates")

# Página de login
@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    csrf_token = generate_csrf_token()
    response = templates.TemplateResponse("login.html", {
        "request": request,
        "csrf_token": csrf_token
    })
    response.set_cookie(key="csrf_token", value=csrf_token, httponly=True, secure=False)
    return response

# Procesar login
@router.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...), csrf_token: str = Form(...)):
    # Verificar CSRF token
    session_csrf = request.cookies.get("csrf_token")
    if not session_csrf or session_csrf != csrf_token:
        simple_logger.security(f"Invalid CSRF token for user: {username}", severity="high", username=username)
        raise HTTPException(status_code=400, detail="Token CSRF inválido")
    
    if authenticate_user(username, password):
        simple_logger.auth(f"User {username} logged in successfully", success=True, username=username)
        simple_metrics.record("auth", "login_success", username=username)
        
        access_token_expires = timedelta(minutes=120)
        access_token = create_access_token(
            data={"sub": username}, expires_delta=access_token_expires
        )
        response = RedirectResponse(url="/dashboard", status_code=302)
        response.set_cookie(
            key="access_token", 
            value=access_token, 
            httponly=True, 
            secure=False,  # Cambiar a True en producción con HTTPS
            max_age=7200  # 2 horas
        )
        return response
    else:
        simple_logger.auth(f"Failed login attempt for user: {username}", success=False, username=username)
        simple_metrics.record("auth", "login_failed", username=username)
        return HTMLResponse(content="Usuario o contraseña incorrectos", status_code=401)

# Dashboard protegido por login
@router.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard(request: Request, current_user: str = Depends(get_current_user)):
    csrf_token = generate_csrf_token()
    response = templates.TemplateResponse("index.html", {
        "request": request, 
        "user": current_user,
        "csrf_token": csrf_token
    })
    response.set_cookie(key="csrf_token", value=csrf_token, httponly=True, secure=False)
    return response

# Cerrar sesión
@router.post("/logout")
async def logout(request: Request):
    try:
        user = get_current_user(request)
        simple_logger.auth(f"User {user} logged out", username=user)
        simple_metrics.record("auth", "logout", username=user)
    except:
        pass
    
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="csrf_token")
    return response