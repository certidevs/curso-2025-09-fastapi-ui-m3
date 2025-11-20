"""
Configuración de la base de datos
"""

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# crear motor de conexión a base de datos
engine = create_engine(
    "sqlite:///cancioncitas.db",
    echo=True,
    connect_args={"check_same_thread": False}
)

# crear fábrica de sesiones de base de datos
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=True,
    expire_on_commit=False
)

# clase base para modelos sqlalchemy
class Base(DeclarativeBase):
    pass

# DEPENDENCIA DE FASTAPI

def get_db():
    db = SessionLocal()
    try:
        yield db # entrega la sesión al endpoint
    finally:
        db.close()


# INICIALIZACIÓN BASE DE DATOS

# método inicializar con canciones por defecto
def init_db():
    """
    Inicializa la base de datos con canciones por defecto si está vacía.
    Sólo crea las canciones si no existen ya en la base de datos.
    """
    from app.models import Song
    
    # crear todas las tablas
    Base.metadata.create_all(engine)
    
    db = SessionLocal()
    try:
        existing_songs = db.execute(select(Song)).scalars().all()
        
        if existing_songs:
            return
        
        default_songs = [
            Song(title="Mamma Mia", artist="ABBA", duration_seconds=300, explicit=False),
            Song(title="Sin ti no soy nada", artist="Amaral", duration_seconds=250, explicit=False),
            Song(title="Sonata para piano nº 14", artist="Ludwig van Beethoven", duration_seconds=800, explicit=False),
            Song(title="Mediterráneo", artist="Joan Manuel Serrat", duration_seconds=400, explicit=False),
            Song(title="Never to Return", artist="Darren Korb", duration_seconds=300, explicit=False),
            Song(title="Billie Jean", artist="Michael Jackson", duration_seconds=294, explicit=False),
            Song(title="Smells Like Teen Spirit", artist="Nirvana", duration_seconds=301, explicit=True)
        ]
        
        # agregar las canciones
        db.add_all(default_songs)
        db.commit()
    finally:
        db.close()