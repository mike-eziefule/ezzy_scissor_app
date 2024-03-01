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
    request:Request,
    db:Session=Depends(database.get_db)
):
    # authenticate if user is logged in
    user = service.get_user_from_token(request, db)
    if not user:
        pass
    return templates.TemplateResponse("faq.html", {"request": request, "user": user})

#features page route
@router.get("/features", response_class = HTMLResponse)
async def features(
    request:Request,
    db:Session=Depends(database.get_db)
):
    
    # authenticate if user is logged in
    user = service.get_user_from_token(request, db)
    if not user:
        pass
    return templates.TemplateResponse("features.html", {"request": request, "user": user})

#login page route
@router.get("/login", response_class=HTMLResponse)
async def authenticationpage(
    request: Request,
    db:Session=Depends(database.get_db)
    ):
    # authenticate if user is logged in
    user = service.get_user_from_token(request, db)
    if not user:
        pass
    return templates.TemplateResponse("login.html", {"request": request, "user": user})

#login page route
@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    db:Session=Depends(database.get_db)
    ):
    
    msg = []
    # authentication
    user = service.get_user_from_token(request, db)
    if not user:
        msg.append("Session expired, Kindly Login")
        return RedirectResponse("ezzy/login", status_code=status.HTTP_302_FOUND)
    
    """View URL."""
    urls = db.query(model.URL).filter(model.URL.owner_id == user.id).all()
    
    base_url = URL(get_settings().base_url)
    
    return templates.TemplateResponse(
        "dashboard.html",{
            "request": request,
            "msg":msg,
            "urls": urls, 
            "user": user,
            "base_url": base_url}
    )

#logout page route
@router.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    
    msg = []
    
    msg.append("Logout successfully")
    response = templates.TemplateResponse("login.html", {"request": request, "msg": msg})
    response.delete_cookie(key="access_token")
    return response

#register page get route
@router.get("/sign-up", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


# #Homepage route
# @router.get("/", response_class=HTMLResponse)
# async def homepage(
#     request: Request,
#     db:Session=Depends(database.get_db)
#     ):
    
#     # authenticate if a user is logged in
#     user = service.get_user_from_token(request, db)
#     if not user:
#         pass
    
#     return templates.TemplateResponse("index.html", {"request": request, "user": user})

