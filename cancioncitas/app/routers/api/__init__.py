"""
Routers de API REST
Contiene los endpoints que devuelven datos en JSON
"""

from app.routers.api import songs
from app.routers.api import concerts

from fastapi import APIRouter

# router principal
router = APIRouter()

# incluir routers en router principal
router.include_router(songs.router)
router.include_router(concerts.router)