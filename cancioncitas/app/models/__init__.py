"""
Modelos de base de datos (SQLAlchemy)
"""

from app.models.song import Song
from app.models.artist import Artist

__all__ = ["Song", "Artist"]