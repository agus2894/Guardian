"""
MÓDULO DE AUTENTICACIÓN Y SEGURIDAD
===================================

CONCEPTOS DE CIBERSEGURIDAD IMPLEMENTADOS:

1. HASH DE CONTRASEÑAS (bcrypt):
   - Las contraseñas nunca se almacenan en texto plano
   - bcrypt incluye salt automático contra ataques rainbow table
   - Resistente a ataques de fuerza bruta por su lentitud intencional

2. TOKENS JWT (JSON Web Tokens):
   - Autenticación sin estado (stateless)
   - Tokens firmados digitalmente para prevenir falsificación
   - Expiración automática para limitar ventana de ataque

3. PROTECCIÓN CSRF:
   - Tokens únicos para prevenir ataques Cross-Site Request Forgery
   - Validación del origen de las peticiones

4. GESTIÓN SEGURA DE SESIONES:
   - Cookies seguras con httpOnly
   - Tokens con tiempo de vida limitado
   - Logout que invalida tokens
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Cookie, Request
import os

# CONFIGURACIÓN DE SEGURIDAD
# Clave secreta para firmar tokens JWT - CRÍTICA para la seguridad
SECRET_KEY = os.getenv("SECRET_KEY", "tu_clave_secreta_muy_segura_aqui")
ALGORITHM = "HS256"  # Algoritmo de cifrado para JWT
ACCESS_TOKEN_EXPIRE_MINUTES = 120  # Duración de sesión en minutos

# CONTEXTO DE CIFRADO DE CONTRASEÑAS
# bcrypt: Algoritmo de hash seguro con salt automático
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    """
    VERIFICACIÓN SEGURA DE CONTRASEÑAS
    - Compara contraseña en texto plano con hash almacenado
    - bcrypt maneja automáticamente el salt y la verificación
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """
    GENERACIÓN DE HASH SEGURO
    - Convierte contraseña a hash irreversible
    - Incluye salt aleatorio único por contraseña
    """
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    CREACIÓN DE TOKEN JWT
    - Genera token firmado digitalmente
    - Incluye información del usuario y tiempo de expiración
    - No almacena información sensible en el token
    """
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
    """
    AUTENTICACIÓN DE USUARIO
    
    Proceso de verificación:
        1. Obtiene credenciales desde variables de entorno
        2. Compara username proporcionado con el configurado
        3. Verifica contraseña usando hash bcrypt o texto plano (demo)
        4. Retorna True si las credenciales son válidas
    
    Configuración soportada:
        - ADMIN_USERNAME/ADMIN_PASSWORD: Para demostración académica
        - GUARDIAN_USER/GUARDIAN_PASS: Compatibilidad legacy
        - Hash de contraseñas para producción
    """
    # CONFIGURACIÓN PRINCIPAL (Preferida)
    valid_user = os.getenv("ADMIN_USERNAME") or os.getenv("GUARDIAN_USER")
    valid_pass_hash = os.getenv("ADMIN_PASSWORD_HASH") or os.getenv("GUARDIAN_PASS_HASH")
    
    if not valid_pass_hash:
        # MODO DEMOSTRACIÓN: Contraseña en texto plano
        # ⚠️ SOLO PARA FINES EDUCATIVOS - NO USAR EN PRODUCCIÓN
        valid_pass_plain = os.getenv("ADMIN_PASSWORD") or os.getenv("GUARDIAN_PASS")
        if username == valid_user and password == valid_pass_plain:
            return True
    else:
        # MODO PRODUCCIÓN: Verificación con hash seguro
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