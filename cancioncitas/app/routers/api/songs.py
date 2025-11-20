"""
Endpoints de API REST
"""

from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Song
from app.schemas import SongResponse, SongCreate, SongUpdate, SongPatch

# crear router para endpoints
router = APIRouter(prefix="/api/songs", tags=["songs"])

# GET - obtener TODAS las canciones
@router.get("", response_model=list[SongResponse])
def find_all(db: Session = Depends(get_db)):
    # db.execute(): ejecuta la consulta
    # select(Song): crea consulta SELECT * FROM song
    # .scalars(): extrae los objetos Song
    # .all(): obtiene los resultados como lista
    return db.execute(select(Song)).scalars().all()

# GET - obtener UNA canción por id
@router.get("/{id}", response_model=SongResponse)
def find_by_id(id: int, db: Session = Depends(get_db)):
    # busca la canción con el id de la ruta
    # .scalar_one_or_none(): devuelve el objeto o None si no existe
    song = db.execute(
        select(Song).where(Song.id == id)
    ).scalar_one_or_none()
    
    if not song:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se ha encontrado la canción con id {id}"
        )
    return song

# POST - crear una nueva canción
@router.post("", response_model=SongResponse, status_code=status.HTTP_201_CREATED)
def create(song_dto: SongCreate, db: Session = Depends(get_db)):
    
    # crea objeto Song con datos validados
    song = Song(
        title=song_dto.title,
        artist=song_dto.artist,
        duration_seconds=song_dto.duration_seconds,
        explicit=song_dto.explicit
    )
    
    db.add(song) # agrega el objeto a la sesión
    db.commit() # confirma la creación en base de datos
    db.refresh(song) # refresca el objeto para obtener el id generado
    return song # retorna la canción creada

# PUT - actualizar COMPLETAMENTE una canción
@router.put("/{id}", response_model=SongResponse)
def update_full(id: int, song_dto: SongUpdate, db: Session = Depends(get_db)):
    # busca canción por id
    song = db.execute(
        select(Song).where(Song.id == id)
    ).scalar_one_or_none()
    
    # si no existe, devuelve 404
    if not song:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se ha encontrado la canción con id {id}"
        )
    
    # guarda el diccionario sacado de song_dto
    update_data = song_dto.model_dump()
    
    # bucle para asignar el valor del diccionario a cada atributo
    for field, value in update_data.items():
        setattr(song, field, value)
    
    db.commit() # confirma los cambios
    db.refresh(song) # refresca el objeto de la base de datos
    return song # retorna la canción actualizada

# PATCH - actualizar PARCIALMENTE una canción
@router.patch("/{id}", response_model=SongResponse)
def update_partial(id: int, song_dto: SongPatch, db: Session = Depends(get_db)):
    # busca canción por id
    song = db.execute(
        select(Song).where(Song.id == id)
    ).scalar_one_or_none()
    
    # si no existe, devuelve 404
    if not song:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se ha encontrado la canción con id {id}"
        )
    
    update_data = song_dto.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(song, field, value)
    
    db.commit() # confirma los cambios en base datos
    db.refresh(song) # refresca el objeto
    return song

# DELETE - eliminar una canción
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(id: int, db: Session = Depends(get_db)):
    # busca la canción por id
    song = db.execute(
        select(Song).where(Song.id == id)
    ).scalar_one_or_none()
    
    # si no existe, devuelve 404
    if not song:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se ha encontrado la canción con id {id}"
        )
    
    # elimina la canción de base de datos
    db.delete(song) # marca el objeto para eliminación
    db.commit() # confirma la eliminación en base de datos
    return None