from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(prefix="/api/concerts", tags=["concerts"])