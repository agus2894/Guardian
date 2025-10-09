from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Cookie, Request
import os

# Configuración de seguridad
SECRET_KEY = os.getenv("SECRET_KEY", "tu_clave_secreta_muy_segura_aqui")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    """Verificar contraseña"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Generar hash de contraseña"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Crear token JWT"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    """Verificar token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except JWTError:
        return None

def authenticate_user(username: str, password: str):
    """Autenticar usuario"""
    valid_user = os.getenv("GUARDIAN_USER")
    valid_pass_hash = os.getenv("GUARDIAN_PASS_HASH")
    
    if not valid_pass_hash:
        # Si no hay hash configurado, usar la contraseña plana (migración)
        valid_pass_plain = os.getenv("GUARDIAN_PASS")
        if username == valid_user and password == valid_pass_plain:
            return True
    else:
        # Usar hash para verificación segura
        if username == valid_user and verify_password(password, valid_pass_hash):
            return True
    
    return False

def get_current_user(request: Request):
    """Obtener usuario actual desde token"""
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No token provided"
        )
    
    username = verify_token(token)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    return username

def generate_csrf_token():
    """Generar token CSRF"""
    from secrets import token_urlsafe
    return token_urlsafe(32)

def verify_csrf_token(request: Request, token: str):
    """Verificar token CSRF"""
    session_token = request.cookies.get("csrf_token")
    return session_token == token