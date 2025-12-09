from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime
from app.models import ConcertStatus
from app.schemas import ArtistResponse

class ConcertResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    price: float
    capacity: int | None
    status: ConcertStatus
    is_sold_out: bool | None
    date_time: datetime
    img_url: str | None
    artist_id: int
    artist: ArtistResponse

class ConcertCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: str
    price: float
    capacity: int | None = None
    status: ConcertStatus = ConcertStatus.SCHEDULED
    is_sold_out: bool | None = False
    date_time: datetime
    img_url: str | None = None
    artist_id: int
    
    @field_validator("name")
    @classmethod
    def validate_name_not_empty(cls, v: str) -> str:
        # verificar si el valor está vacío o sólo tiene espacios
        if not v or not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        
        # verificar longitud máxima
        if len(v.strip()) > 200:
            raise ValueError("El nombre no puede tener más de 200 caracteres")
        
        # retornar el valor normalizado
        return v.strip()
    
    @field_validator("price")
    @classmethod
    def validate_price_positive(cls, v: float) -> float:
        if v < 0:
            raise ValueError("El precio debe ser un número positivo")
        
        return v
    
    @field_validator("capacity")
    @classmethod
    def validate_capacity_positive(cls, v: int | None) -> int | None:
        if v is not None and v < 0:
            raise ValueError("La capacidad debe ser un número positivo")
        
        return v
    
    @field_validator("img_url")
    @classmethod
    def validate_img_url_length(cls, v: str | None) -> str | None:
        if v is not None and len(v) > 500:
            raise ValueError("La url de la imagen no puede tener más de 500 caracteres")
        
        return v
    
    @field_validator("artist_id")
    @classmethod
    def validate_artist_id_positive(cls, v: int) -> int:
        if v < 1:
            raise ValueError("El id del artista debe ser un número positivo")
        
        return v