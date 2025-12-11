from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Form, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select

from app.database import get_db
from app.models import Concert

templates = Jinja2Templates(directory="app/templates")

router = APIRouter(prefix="/concerts", tags=["web"])

@router.get("", response_class=HTMLResponse)
def list_concerts(request: Request, db: Session = Depends(get_db)):
    concerts = db.execute(
        select(Concert).options(joinedload(Concert.artist))
    ).scalars().unique().all()
    
    return templates.TemplateResponse(
        "concerts/list.html",
        {"request": request, "concerts": concerts}
    )