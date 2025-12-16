from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Form, HTTPException, Query, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, select
from datetime import datetime

from app.database import get_db
from app.models import Concert, Artist, ConcertStatus

templates = Jinja2Templates(directory="app/templates")

router = APIRouter(prefix="/concerts", tags=["web"])

@router.get("", response_class=HTMLResponse)
def list_concerts(
    request: Request, 
    db: Session = Depends(get_db),
    name: str | None = Query(None, description="Filtro por nombre del concierto"),
    artist_id: str | None = Query(None, description="Filtro por ID del artista"),
    future_only: str | None = Query(None, description="Mostrar solo conciertos futuros")
):
    query = select(Concert).options(joinedload(Concert.artist))
    
    conditions = []
    
    if name and name.strip():
        conditions.append(Concert.name.ilike(f"%{name.strip()}%"))
    
    artist_id_value = None
    if artist_id and artist_id.strip():
        try:
            artist_id_value = int(artist_id.strip())
            conditions.append(Concert.artist_id == artist_id_value)
        except ValueError:
            pass
    
    future_only_value = False
    if future_only and future_only.strip().lower() in ("true", "1", "on", "yes"):
        future_only_value = True
        now = datetime.now()
        conditions.append(Concert.date_time >= now)
    
    if conditions:
        query = query.where(and_(*conditions))
    
    concerts = db.execute(query).scalars().unique().all()
    
    artists = db.execute(select(Artist).order_by(Artist.name)).scalars().all()
    
    return templates.TemplateResponse(
        "concerts/list.html",
        {
            "request": request, 
            "concerts": concerts,
            "artists": artists,
            "filter_name": name or "",
            "filter_artist_id": artist_id_value,
            "filter_future_only": future_only_value
        }
    )

@router.get("/new", response_class=HTMLResponse)
def show_create_form(request: Request, db: Session = Depends(get_db)):
    artists = db.execute(select(Artist)).scalars().all()
    
    return templates.TemplateResponse(
        "concerts/form.html",
        {"request": request, "concert": None, "artists": artists, "statuses": ConcertStatus}
    )

@router.post("/new", response_class=HTMLResponse)
def create_concert(
    request: Request,
    name: str = Form(...),
    price: str = Form(...),
    capacity: str = Form(None),
    status: str = Form(...),
    is_sold_out: str = Form(None),
    date_time: str = Form(...),
    img_url: str = Form(None),
    artist_id: str = Form(...),
    db: Session = Depends(get_db)
):
    errors = []
    form_data = {
        "name": name,
        "price": price,
        "capacity": capacity,
        "status": status,
        "is_sold_out": is_sold_out,
        "date_time": date_time,
        "img_url": img_url,
        "artist_id": artist_id
    }
    
    artists = db.execute(select(Artist)).scalars().all()
    
    price_value = None
    if price and price.strip():
        try:
            price_value = float(price.strip())
            if price_value < 0:
                errors.append("El precio debe ser un número positivo")
        except ValueError:
            errors.append("El precio debe ser un número válido")
    else:
        errors.append("El precio es requerido")
    
    capacity_value = None
    if capacity and capacity.strip():
        try:
            capacity_value = int(capacity.strip())
            if capacity_value < 0:
                errors.append("La capacidad debe ser un número positivo")
        except ValueError:
            errors.append("La capacidad debe ser un número válido")
    
    status_value = None
    try:
        status_value = ConcertStatus(status)
    except ValueError:
        errors.append("El estado debe ser scheduled, cancelled o completed")
    
    is_sold_out_value = False
    if is_sold_out and (is_sold_out == "true" or is_sold_out == "on"):
        is_sold_out_value = True
    
    datetime_value = None
    if date_time and date_time.strip():
        try:
            datetime_value = datetime.strptime(date_time.strip(), "%Y-%m%dT%H:%M")
        except ValueError:
            errors.append("La fecha y hora deben tener el formato YYYY-MM-DDTHH:MM")
    else:
        errors.append("La fecha y hora es requerida")
    
    img_url_value = None
    if img_url and img_url.strip():
        img_url_value = img_url.strip()
        if len(img_url_value) > 500:
            errors.append("La URL de imagen no puede tener más de 500 caracteres")
    
    artist_id_value = None
    if artist_id and artist_id.strip():
        try:
            artist_id_value = int(artist_id.strip())
            if artist_id_value < 1:
                errors.append("El id del artista tiene que ser un número positivo")
            artist = db.execute(select(Artist).where(Artist.id == artist_id_value)).scalar_one_or_none()
            if not artist:
                errors.append("El artista seleccionado no existe")
        except ValueError:
            errors.append("El id del artista tiene que ser un número válido")
    else:
        errors.append("El id del artista es requerido")
    
    if not name or not name.strip():
        errors.append("El nombre es requerido")
    elif len(name.strip()) > 200:
        errors.append("El nombre no puede exceder los 200 caracteres")
    
    if errors:
        return templates.TemplateResponse(
            "concerts/form.html",
            {"request": request, "concert": None, "artists": artists, "statuses": ConcertStatus, "errors": errors, "form_data": form_data}
        )
    
    try:
        concert = Concert(
            name=name.strip(),
            price=price_value,
            capacity=capacity_value,
            status=status_value,
            is_sold_out=is_sold_out_value,
            date_time=datetime_value,
            img_url=img_url_value,
            artist_id=artist_id_value
        )
        
        db.add(concert)
        db.commit()
        db.refresh(concert)
        
        return RedirectResponse(url=f"/concerts/{concert.id}", status_code=303)
    
    except Exception as e:
        db.rollback()
        errors.append(f"Error al crear el concierto: {str(e)}")
        return templates.TemplateResponse(
            "concerts/form.html",
            {"request": request, "concert": None, "artists": artists, "statuses": ConcertStatus, "errors": errors, "form_data": form_data}
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

@router.post("/{concert_id}/edit", response_class=HTMLResponse)
def update_concert(
    request: Request,
    concert_id: int,
    name: str = Form(...),
    price: str = Form(...),
    capacity: str = Form(None),
    status: str = Form(...),
    is_sold_out: str = Form(None),
    date_time: str = Form(...),
    img_url: str = Form(None),
    artist_id: str = Form(...),
    db: Session = Depends(get_db)
):
    concert = db.execute(
        select(Concert)
        .where(Concert.id == concert_id)
        .options(joinedload(Concert.artist))
    ).scalar_one_or_none()
    
    if concert is None:
        raise HTTPException(status_code=404, detail="Concierto no encontrado")
    
    errors = []
    form_data = {
        "name": name,
        "price": price,
        "capacity": capacity,
        "status": status,
        "is_sold_out": is_sold_out,
        "date_time": date_time,
        "img_url": img_url,
        "artist_id": artist_id
    }
    
    artists = db.execute(select(Artist)).scalars().all()
    
    price_value = None
    if price and price.strip():
        try:
            price_value = float(price.strip())
            if price_value < 0:
                errors.append("El precio debe ser un número positivo")
        except ValueError:
            errors.append("El precio debe ser un número válido")
    else:
        errors.append("El precio es requerido")
    
    capacity_value = None
    if capacity and capacity.strip():
        try:
            capacity_value = int(capacity.strip())
            if capacity_value < 0:
                errors.append("La capacidad debe ser un número positivo")
        except ValueError:
            errors.append("La capacidad debe ser un número válido")
    
    status_value = None
    try:
        status_value = ConcertStatus(status)
    except ValueError:
        errors.append("El estado debe ser scheduled, cancelled o completed")
    
    is_sold_out_value = False
    if is_sold_out and (is_sold_out == "true" or is_sold_out == "on"):
        is_sold_out_value = True
    
    datetime_value = None
    if date_time and date_time.strip():
        try:
            datetime_value = datetime.strptime(date_time.strip(), "%Y-%m%dT%H:%M")
        except ValueError:
            errors.append("La fecha y hora deben tener el formato YYYY-MM-DDTHH:MM")
    else:
        errors.append("La fecha y hora es requerida")
    
    img_url_value = None
    if img_url and img_url.strip():
        img_url_value = img_url.strip()
        if len(img_url_value) > 500:
            errors.append("La URL de imagen no puede tener más de 500 caracteres")
    
    artist_id_value = None
    if artist_id and artist_id.strip():
        try:
            artist_id_value = int(artist_id.strip())
            if artist_id_value < 1:
                errors.append("El id del artista tiene que ser un número positivo")
            artist = db.execute(select(Artist).where(Artist.id == artist_id_value)).scalar_one_or_none()
            if not artist:
                errors.append("El artista seleccionado no existe")
        except ValueError:
            errors.append("El id del artista tiene que ser un número válido")
    else:
        errors.append("El id del artista es requerido")
    
    if not name or not name.strip():
        errors.append("El nombre es requerido")
    elif len(name.strip()) > 200:
        errors.append("El nombre no puede exceder los 200 caracteres")
    
    if errors:
        return templates.TemplateResponse(
            "concerts/form.html",
            {"request": request, "concert": concert, "artists": artists, "statuses": ConcertStatus, "errors": errors, "form_data": form_data}
        )
    
    try:
        concert.name=name.strip(),
        concert.price=price_value,
        concert.capacity=capacity_value,
        concert.status=status_value,
        concert.is_sold_out=is_sold_out_value,
        concert.date_time=datetime_value,
        concert.img_url=img_url_value,
        concert.artist_id=artist_id_value
        
        db.commit()
        db.refresh(concert)
        
        return RedirectResponse(url=f"/concerts/{concert.id}", status_code=303)
    
    except Exception as e:
        db.rollback()
        errors.append(f"Error al actualizar el concierto: {str(e)}")
        return templates.TemplateResponse(
            "concerts/form.html",
            {"request": request, "concert": concert, "artists": artists, "statuses": ConcertStatus, "errors": errors, "form_data": form_data}
        )