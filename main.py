from fastapi import FastAPI
from routers import scan
from db.database import init_db
from fastapi.responses import RedirectResponse

app = FastAPI(title="Guardián - Sistema de Monitoreo de Red")

# Registrar rutas
app.include_router(scan.router)

init_db()  # Esto asegura que la DB esté lista al iniciar FastAPI

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")
