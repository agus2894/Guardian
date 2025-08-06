from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from db.whitelist import get_whitelist, add_to_whitelist

router = APIRouter(prefix="/whitelist", tags=["Whitelist"])

# Obtener todos los dispositivos permitidos
@router.get("/")
async def listar_whitelist():
    data = get_whitelist()
    return {"whitelist": data}

# Agregar un nuevo dispositivo a la whitelist
@router.post("/agregar")
async def agregar_dispositivo(
    nombre: str = Form(...),
    ip: str = Form(...)
):
    add_to_whitelist(nombre, ip)
    return JSONResponse(content={"mensaje": "Dispositivo agregado a whitelist"}, status_code=200)
