from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from db.whitelist import get_whitelist, add_to_whitelist

router = APIRouter(prefix="/whitelist", tags=["Whitelist"])

# Obtener todos los dispositivos de la whitelist
@router.get("/")
async def listar_whitelist():
    data = get_whitelist()
    return {"whitelist": data}

# Agregar un nuevo dispositivo a la whitelist (sin MAC)
@router.post("/add")  # <-- ¡COINCIDE con el HTML!
async def agregar_dispositivo(
    nombre: str = Form(...),
    ip: str = Form(...)
):
    add_to_whitelist(nombre=nombre, mac="", ip=ip)  # Mac vacía
    return JSONResponse(content={"mensaje": "Dispositivo agregado a whitelist"}, status_code=200)
