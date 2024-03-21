"""Routes related to browsing webpages"""

from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from storage import database, model
from sqlalchemy.orm import Session
from utils import service
from starlette.datastructures import URL
from config.config import get_settings


router = APIRouter(prefix="/ezzy", tags=["Webpages"])

templates = Jinja2Templates(directory="templates")

#faq page route
@router.get("/faq", response_class = HTMLResponse)
async def faq_page(
    request:Request,
):
    return templates.TemplateResponse("faq.html", {"request": request})

#features page route
@router.get("/features", response_class = HTMLResponse)
async def features(
    request:Request,
):
    
    return templates.TemplateResponse("features.html", {"request": request})


#dashboard page route
@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    db:Session=Depends(database.get_db)
    ):
    
    user = service.get_user_from_token(request, db)
    if not user:
        return RedirectResponse("/auth/login")
    
    """View URL."""
    urls = db.query(model.URL).filter(model.URL.owner_id == user.id).all()
    
    base_url = URL(get_settings().base_url)
    
    return templates.TemplateResponse(
        "dashboard.html",{
        "request": request,
        "urls": urls, 
        "user": user,
        "base_url": base_url}
    )



