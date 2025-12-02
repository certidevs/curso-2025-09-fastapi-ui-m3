from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Form, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
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

# mostrar formulario crear
@router.get("/new", response_class=HTMLResponse)
def show_create_form(request: Request):
    return templates.TemplateResponse(
        "songs/form.html",
        {"request": request, "song": None}
    )

# crear nueva canción
@router.post("/new", response_class=HTMLResponse)
def create_song(
    request: Request,
    title: str = Form(...),
    artist: str = Form(...),
    duration_seconds: str = Form(None),
    explicit: str = Form(""),
    db: Session = Depends(get_db)
):
    errors = []
    form_data = {
        "title": title,
        "artist": artist,
        "duration_seconds": duration_seconds,
        "explicit": explicit
    }
    
    # validar y convertir duration_seconds
    duration_value = None
    if duration_seconds and duration_seconds.strip():
        try:
            duration_value = int(duration_seconds)
            if duration_value < 0:
                errors.append("La duración debe ser un número positivo")
        except ValueError:
            errors.append("La duración debe ser un número válido")
    
    # validar explicit
    explicit_value = None
    if explicit == "true":
        explicit_value = True
    elif explicit == "false":
        explicit_value = False
    
    # validar campos obligatorios
    if not title or not title.strip():
        errors.append("El título es requerido")
    if not artist or not artist.strip():
        errors.append("El artista es requerido")
    
    # si hay errores, mostrar el formulario con los errores
    if errors:
        return templates.TemplateResponse(
            "songs/form.html",
            {"request": request, "song": None, "errors": errors, "form_data": form_data}
        )
    
    # crear la canción
    try:
        song = Song(
            title = title.strip(),
            artist = artist.strip(),
            duration_seconds = duration_value,
            explicit = explicit_value
        )
        db.add(song)
        db.commit()
        db.refresh(song)
        
        # redirigir a pantalla detalle
        return RedirectResponse(url=f"/songs/{song.id}", status_code=303)
    except Exception as e:
        db.rollback()
        errors.append(f"Error al crear la canción: {str(e)}")
        return templates.TemplateResponse(
            "songs/form.html",
            {"request": request, "song": None, "errors": errors, "form_data": form_data}
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

# mostrar formulario editar
@router.get("/{song_id}/edit", response_class=HTMLResponse)
def show_edit_form(request: Request, song_id: int, db: Session = Depends(get_db)):
    # obtener canción por id
    song = db.execute(select(Song).where(Song.id == song_id)).scalar_one_or_none()
    
    # lanzar error 404 si no existe canción
    if song is None:
        raise HTTPException(status_code=404, detail="404 - Canción  no encontrada")
    
    return templates.TemplateResponse(
        "songs/form.html",
        {"request": request, "song": song}
    )

# editar canción existente
@router.post("/{song_id}/edit", response_class=HTMLResponse)
def update_song(
    request: Request,
    song_id: int,
    title: str = Form(...),
    artist: str = Form(...),
    duration_seconds: str = Form(None),
    explicit: str = Form(""),
    db: Session = Depends(get_db)
):
    song = db.execute(select(Song).where(Song.id == song_id)).scalar_one_or_none()
    
    if song is None:
        raise HTTPException(status_code=404, detail="404 - Canción no encontrada")
    
    errors = []
    form_data = {
        "title": title,
        "artist": artist,
        "duration_seconds": duration_seconds,
        "explicit": explicit
    }
    
    duration_value = None
    if duration_seconds and duration_seconds.strip():
        try:
            duration_value = int(duration_seconds)
            if duration_value < 0:
                errors.append("La duración debe ser un número positivo")
        except ValueError:
            errors.append("La duración debe ser un número válido")
    
    explicit_value = None
    if explicit == "true":
        explicit_value = True
    elif explicit == "false":
        explicit_value = False
    
    if not title or not title.strip():
        errors.append("El título es requerido")
    if not artist or not artist.strip():
        errors.append("El artista es requerido")
    
    if errors:
        return templates.TemplateResponse(
            "songs/form.html",
            {"request": request, "song": song, "errors": errors, "form_data": form_data}
        )
    
    try:
        song.title = title.strip()
        song.artist = artist.strip()
        song.duration_seconds = duration_value
        song.explicit = explicit_value

        db.commit()
        db.refresh(song)
        
        return RedirectResponse(url=f"/songs/{song.id}", status_code=303)
    except Exception as e:
        db.rollback()
        errors.append(f"Error al actualizar la canción: {str(e)}")
        return templates.TemplateResponse(
            "songs/form.html",
            {"request": request, "song": song, "errors": errors, "form_data": form_data}
        )