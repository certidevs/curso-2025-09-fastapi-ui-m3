from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime

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

# crear nuevo artista
@router.post("/new", response_class=HTMLResponse)
def create_artist(
    request: Request,
    name: str = Form(...),
    birth_date: str = Form(None),
    db: Session = Depends(get_db)
):
    errors = []
    form_data = {
        "name": name,
        "birth_date": birth_date
    }
    
    birth_date_value = None
    if birth_date and birth_date.strip():
        try:
            birth_date_value = datetime.strptime(birth_date.strip(), "%Y-%m-%d")
        except ValueError:
            errors.append("La fecha de nacimiento tiene que tener el formato YYYY-MM-DD")
    
    if not name or not name.strip():
        errors.append("El nombre es requerido")
    
    if errors:
        return templates.TemplateResponse(
            "artists/form.html",
            {"request": request, "artist": None, "errors": errors, "form_data": form_data}
        )
    
    try:
        artist = Artist(
            name=name.strip(),
            birth_date=birth_date_value
        )
        db.add(artist)
        db.commit()
        db.refresh(artist)
        
        return RedirectResponse(url=f"/artists/{artist.id}", status_code=303)
    except Exception as e:
        db.rollback()
        errors.append(f"Error al crear el artista: {str(e)}")
        return templates.TemplateResponse(
            "artists/form.html",
            {"request": request, "artist": None, "errors": errors, "form_data": form_data}
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