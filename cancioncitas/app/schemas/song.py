"""
Esquemas Pydantic para estructura y validación
"""

from pydantic import BaseModel, ConfigDict, field_validator

# schema para TODAS las respuestas de la API
# lo usamos en GET, POST, PUT, PATCH
class SongResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    title: str
    artist: str
    duration_seconds: int | None
    explicit: bool | None

# schema para CREAR una canción (POST)
# no incluimos id porque se genera automáticamente
class SongCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    title: str
    artist: str
    duration_seconds: int | None = None
    explicit: bool | None = None
    
    @field_validator("title", "artist")
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        # verificar si el valor está vacío o sólo tiene espacios
        if not v or not v.strip():
            raise ValueError("Este campo no puede estar vacío")

        # retorna el valor sin espacios al principio y al final (normalizar)
        return v.strip()
    
    @field_validator("duration_seconds")
    @classmethod
    def validate_duration_positive(cls, v: int | None) -> int | None:
        # valida sólo si se da un valor (no es None)
        if v is not None and v < 0:
            raise ValueError("La duración debe ser un número positivo")
        
        return v
        

# schema para ACTUALIZACIÓN COMPLETA (PUT)
# todos los campos se tienen que enviar
class SongUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    title: str
    artist: str
    duration_seconds: int | None
    explicit: bool | None
    
    @field_validator("title", "artist")
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Este campo no puede estar vacío")
        
        return v.strip()
    
    @field_validator("duration_seconds")
    @classmethod
    def validate_duration_positive(cls, v: int | None) -> int | None:
        if v is not None and v < 0:
            raise ValueError("La duración debe ser un número positivo")
        
        return v

# schema para ACTUALIZACIÓN PARCIAL (PATCH)
# sólo se envían los campos que quieras actualizar
class SongPatch(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    title: str | None = None
    artist: str | None = None
    duration_seconds: int | None = None
    explicit: bool | None = None
    
    @field_validator("title", "artist")
    @classmethod
    def validate_not_empty(cls, v: str | None) -> str | None:
        # si no se proporcionó valor (None), no validamos
        if v is None:
            return None
        
        # si se proporcionó valor, validamos que no esté vacío
        if not v or not v.strip():
            raise ValueError("Este campo no puede estar vacío")
        
        return v.strip()
    
    @field_validator("duration_seconds")
    @classmethod
    def validate_duration_positive(cls, v: int | None) -> int | None:
        if v is None:
            return None
        
        if v < 0:
            raise ValueError("La duración debe ser un número positivo")
        
        return v