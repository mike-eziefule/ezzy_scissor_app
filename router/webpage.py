"""Routes related to browsing webpages"""

from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


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

#login page route
@router.get("/create_url", response_class=HTMLResponse)
async def authenticationpage(request: Request):
    return templates.TemplateResponse("create_url.html", {"request": request})

#login page route
@router.get("/dashboard", response_class=HTMLResponse)
async def authenticationpage(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


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

#register page route
@router.get("/edit_url", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("customize.html", {"request": request})
