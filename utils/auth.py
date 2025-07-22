from fastapi import Request, HTTPException
from starlette.responses import RedirectResponse
import os

USERNAME = os.getenv("GUARDIAN_USER", "admin")
PASSWORD = os.getenv("GUARDIAN_PASS", "admin123")

def check_login(request: Request):
    session = request.cookies.get("session")
    if session != "active":
        raise HTTPException(status_code=401, detail="No autorizado")

def login_user(username, password):
    if username == USERNAME and password == PASSWORD:
        return True
    return False
