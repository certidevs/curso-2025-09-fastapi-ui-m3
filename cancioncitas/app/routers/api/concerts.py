from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models import Concert
from app.schemas import ConcertResponse

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