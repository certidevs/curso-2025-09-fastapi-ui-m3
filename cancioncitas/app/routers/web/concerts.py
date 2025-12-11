from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Form, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database import get_db

templates = Jinja2Templates(directory="app/templates")

router = APIRouter(prefix="/concerts", tags=["web"])