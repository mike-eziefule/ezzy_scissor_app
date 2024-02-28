"""Routes related to browsing webpages"""

from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from storage import database, model
from sqlalchemy.orm import Session
from utils import crud, service
from starlette.datastructures import URL
from config.config import get_settings


router = APIRouter(prefix="/ezzy", tags=["Webpages"])

templates = Jinja2Templates(directory="templates")


#faq page route
@router.get("/faq", response_class = HTMLResponse)
async def faq_page(
    request:Request
):
    return templates.TemplateResponse("faq.html", {"request": request})

#features page route
@router.get("/features", response_class = HTMLResponse)
async def features(
    request:Request
):
    return templates.TemplateResponse("features.html", {"request": request})

#login page route
@router.get("/login", response_class=HTMLResponse)
async def authenticationpage(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# #login page route
# @router.get("/create_url", response_class=HTMLResponse)
# async def create_url(request: Request):
#     return templates.TemplateResponse("create_url.html", {"request": request})

#login page route
@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    db:Session=Depends(database.get_db)
    ):
    
    # authentication
    user = service.get_user_from_token(request, db)
    if not user:
        return RedirectResponse("ezzy/login", status_code=status.HTTP_302_FOUND)
    
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


#logout page route
@router.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    msg = "Logout successfully"
    response = templates.TemplateResponse("login.html", {"request": request, "msg": msg})
    response.delete_cookie(key="access_token")
    return response

#register page route
@router.get("/sign-up", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

#register page route
@router.get("/", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

