from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models import Concert
from app.schemas import ConcertResponse, ConcertCreate

router = APIRouter(prefix="/api/concerts", tags=["concerts"])

# obtener todos los conciertos
@router.get("", response_model=list[ConcertResponse])
def find_all(db: Session = Depends(get_db)):
    return db.execute(
        select(Concert).options(joinedload(Concert.artist))
    ).scalars().unique().all()

# obtener un concierto
@router.get("/{id}", response_model=ConcertResponse)
def find_by_id(id: int, db: Session = Depends(get_db)):
    concert = db.execute(
        select(Concert)
        .where(Concert.id == id)
        .options(joinedload(Concert.artist))
    ).scalar_one_or_none()
    
    if not concert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se ha encontrado el concierto con id {id}"
        )
    
    return concert

# crear un nuevo concierto
@router.post("", response_model=ConcertResponse, status_code=status.HTTP_201_CREATED)
def create(concert_dto: ConcertCreate, db: Session = Depends(get_db)):
    
    concert = Concert(
        name=concert_dto.name,
        price=concert_dto.price,
        capacity=concert_dto.capacity,
        status=concert_dto.status,
        is_sold_out=concert_dto.is_sold_out,
        date_time=concert_dto.date_time,
        img_url=concert_dto.img_url,
        artist_id=concert_dto.artist_id
    )
    
    db.add(concert)
    db.commit()
    db.refresh(concert)
    
    concert_with_artist = db.execute(
        select(Concert)
        .where(Concert.id == concert.id)
        .options(joinedload(Concert.artist))
    ).scalar_one()
    
    return concert_with_artist