import enum
from sqlalchemy import Integer, String, Float, Enum, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.database import Base
from app.models import Artist

class ConcertStatus(enum.Enum):
    SCHEDULED = "scheduled"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class Concert(Base):
    __tablename__ = "concerts"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    
    price: Mapped[float] = mapped_column(Float, nullable=False)
    
    capacity: Mapped[int | None] = mapped_column(Integer, nullable=True)
    
    status: Mapped[ConcertStatus] = mapped_column(Enum(ConcertStatus), 
                                                  nullable=False, default=ConcertStatus.SCHEDULED)
    is_sold_out: Mapped[bool | None] = mapped_column(Boolean, nullable=True, default=False)
    
    date_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    
    img_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    
    artist_id: Mapped[int] = mapped_column(Integer, ForeignKey("artists.id"), nullable=False)
    
    artist: Mapped["Artist"] = relationship("Artist")