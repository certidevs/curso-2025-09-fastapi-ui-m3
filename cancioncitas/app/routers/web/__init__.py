"""
Router de páginas web
Contienen los endpoints que renderizan HTMLs
"""

from app.routers.web import home
from app.routers.web import songs

from fastapi import APIRouter

router = APIRouter()

router.include_router(home.router)
router.include_router(songs.router)