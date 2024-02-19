"""Routes related to browsing webpages"""

from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter(prefix="/pages", tags=["Webpages"])

templates = Jinja2Templates(directory="templates")

#RETURN FAQ PAGE
@router.get("/faq", response_class = HTMLResponse)
async def faq_page(
    request:Request
):
    return templates.TemplateResponse("faq.html", {"request": request})

#RETURN FEATURES PAGE
@router.get("/features", response_class = HTMLResponse)
async def features(
    request:Request
):
    return templates.TemplateResponse("features.html", {"request": request})
