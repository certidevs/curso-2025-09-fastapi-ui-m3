from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

# configuración de Jinja2Templates
templates = Jinja2Templates(directory="app/templates")

# router para rutas web
router = APIRouter(prefix="/artists", tags=["web"])