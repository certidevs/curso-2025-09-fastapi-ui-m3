from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database import get_db
from app.models import Song

# configuración de Jinja2Templates
templates = Jinja2Templates(directory="app/templates")

# router para rutas web
router = APIRouter(prefix="/songs", tags=["web"])

# listar canciones (http://localhost:8000/songs)
@router.get("", response_class=HTMLResponse)
def list_songs(request: Request, db: Session = Depends(get_db)):
    songs = db.execute(select(Song)).scalars().all()
    
    return templates.TemplateResponse(
        "songs/list.html",
        {"request": request, "songs": songs}
    )

# detalle canción (http://localhost:8000/songs/5)
@router.get("/{song_id}", response_class=HTMLResponse)
def song_detail(request: Request, song_id: int, db: Session = Depends(get_db)):
    song = db.execute(select(Song).where(Song.id == song_id)).scalar_one_or_none()
    
    if song is None:
        raise HTTPException(status_code=404, detail="404 - Canción no encontrada")
    
    return templates.TemplateResponse(
        "songs/detail.html",
        {"request": request, "song": song}
    )