from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Form, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select

from app.database import get_db
from app.models import Concert, Artist, ConcertStatus

templates = Jinja2Templates(directory="app/templates")

router = APIRouter(prefix="/concerts", tags=["web"])

@router.get("", response_class=HTMLResponse)
def list_concerts(request: Request, db: Session = Depends(get_db)):
    concerts = db.execute(
        select(Concert).options(joinedload(Concert.artist))
    ).scalars().unique().all()
    
    return templates.TemplateResponse(
        "concerts/list.html",
        {"request": request, "concerts": concerts}
    )

@router.get("/new", response_class=HTMLResponse)
def show_create_form(request: Request, db: Session = Depends(get_db)):
    artists = db.execute(select(Artist)).scalars().all()
    
    return templates.TemplateResponse(
        "concerts/form.html",
        {"request": request, "concert": None, "artists": artists, "statuses": ConcertStatus}
    )

@router.get("/{concert_id}", response_class=HTMLResponse)
def concert_detail(request: Request, concert_id: int, db: Session = Depends(get_db)):
    concert = db.execute(
        select(Concert)
        .where(Concert.id == concert_id)
        .options(joinedload(Concert.artist))
    ).scalar_one_or_none()
    
    if concert is None:
        raise HTTPException(status_code=404, detail="Concierto no encontrado")
    
    return templates.TemplateResponse(
        "concerts/detail.html",
        {"request": request, "concert": concert}
    )

@router.get("/{concert_id}/edit", response_class=HTMLResponse)
def show_edit_form(request: Request, concert_id: int, db: Session = Depends(get_db)):
    concert = db.execute(
        select(Concert)
        .where(Concert.id == concert_id)
        .options(joinedload(Concert.artist))
    ).scalar_one_or_none()
    
    if concert is None:
        raise HTTPException(status_code=404, detail="Concierto no encontrado")
    
    artists = db.execute(select(Artist)).scalars().all()
    
    return templates.TemplateResponse(
        "concerts/form.html",
        {"request": request, "concert": concert, "artists": artists, "statuses": ConcertStatus}
    )