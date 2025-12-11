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