from fastapi import APIRouter, Form, Depends
from fastapi.responses import JSONResponse
from utils.auth import get_current_user
from db.whitelist import get_whitelist, add_to_whitelist

router = APIRouter(prefix="/whitelist", tags=["Whitelist"])

@router.get("/")
async def listar_whitelist(current_user: str = Depends(get_current_user)):
    data = get_whitelist()
    return {"whitelist": data}
@router.post("/agregar")
async def agregar_dispositivo(
    nombre: str = Form(...),
    ip: str = Form(...),
    mac: str = Form(None),
    current_user: str = Depends(get_current_user)
):
    add_to_whitelist(nombre, ip, mac)
    return JSONResponse(content={"mensaje": "Dispositivo agregado a whitelist"}, status_code=200)
