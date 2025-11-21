from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import get_db
from app.models import Song

templates = Jinja2Templates(directory="app/templates")

router = APIRouter(prefix="/songs", tags=["web"])

# listar canciones (http://localhost:8000/songs)
@router.get("", response_class=HTMLResponse)
def list_songs(request: Request, db: Session = Depends(get_db)):
    songs = db.execute(select(Song)).scalars().all()
    
    return templates.TemplateResponse(
        "songs/list.html",
        {"request": request, "songs": songs}
    )