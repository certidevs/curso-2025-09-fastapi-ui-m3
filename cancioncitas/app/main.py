"""
Configuración de la aplicación FastAPI
"""

from fastapi import FastAPI
from app.database import init_db
from app.routers.api import router as api_router

# crea la instancia de la aplicación FastAPI
app = FastAPI(title="Cancioncitas", version="1.0.0")

# inicializa la base de datos con canciones por defecto
init_db()

# registrar los routers
app.include_router(api_router)


"""
# endpoint raíz
@app.get("/")
def home():
    return {"mensaje": "Bienvenido a la app Cancioncitas"}
"""