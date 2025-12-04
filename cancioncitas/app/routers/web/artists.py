from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database import get_db
from app.models import Artist

# configuración de Jinja2Templates
templates = Jinja2Templates(directory="app/templates")

# router para rutas web
router = APIRouter(prefix="/artists", tags=["web"])

# listar aristas (http://localhost:8000/artists)
@router.get("", response_class=HTMLResponse)
def list_artists(request: Request, db: Session = Depends(get_db)):
    artists = db.execute(select(Artist)).scalars().all()
    
    return templates.TemplateResponse(
        "artists/list.html",
        {"request": request, "artists": artists}
    )

# mostrar formulario crear
@router.get("/new", response_class=HTMLResponse)
def show_create_form(request: Request):
    return templates.TemplateResponse(
        "artists/form.html",
        {"request": request, "artist": None}
    )

# detalle artista (http://localhost:8000/artists/5)
@router.get("/{artist_id}", response_class=HTMLResponse)
def artist_detail(request: Request, artist_id: int, db: Session = Depends(get_db)):
    artist = db.execute(select(Artist).where(Artist.id == artist_id)).scalar_one_or_none()
    
    if artist is None:
        raise HTTPException(status_code=404, detail="404 - Artista no encontrado")
    
    return templates.TemplateResponse(
        "artists/detail.html",
        {"request": request, "artist": artist}
    )