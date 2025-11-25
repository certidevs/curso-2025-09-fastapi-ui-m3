from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.database import Base

class Artist(Base):
    __tablename__ = "artists"
    
    # clave primaria, se genera automáticamente
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # requerido, máximo 200 caracteres
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    # opcional
    birth_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)