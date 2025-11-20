from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

# modelo de la tabla song (se crea sólo un modelo, que será una tabla en nuestra base de datos)
class Song(Base):
    __tablename__ = "songs" # nombre de la tabla en bd
    
    # clave primaria, se genera automáticamente
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # requerido, máximo 200 caracteres
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    # requerido, máximo 200 caracteres
    artist: Mapped[str] = mapped_column(String(200), nullable=False)
    # opcional
    duration_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # opcional
    explicit: Mapped[bool | None] = mapped_column(Boolean, nullable=True)