"""Routes related to URL adding and listing"""

import validators
from fastapi import APIRouter, Request, Depends, status, Form, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from storage import database, model
from utils import crud, service
from starlette.datastructures import URL
from config.config import get_settings
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from starlette.background import BackgroundTasks
import os

router = APIRouter(tags=["url"])


templates = Jinja2Templates(directory="templates")

def remove_file(path: str) -> None:
    os.unlink(path)
    
#VIEW URL BY KEY
@router.get("/", response_class = HTMLResponse)
async def homepage(
    request:Request,
):
    return templates.TemplateResponse("index.html", {"request": request})

#create_url GET ROUTE
@router.get("/create_url", response_class=HTMLResponse)
async def create_url(
    request: Request,
    db:Session=Depends(database.get_db)
    ):
    
    # authentication
    user = service.get_user_from_token(request, db)
    if not user:
        msg = []
        
        msg.append("Session Expired, Login")
        return templates.TemplateResponse("login.html", {"request": request, "user": user})
    
    
    return templates.TemplateResponse(
        "create_url.html", 
        {"request": request, "user": user}
    )
    
#create_url POST ROUTE
@router.post("/create_url", response_class=HTMLResponse)
async def create_url_post(
    request: Request,
    target_url: str = Form(...),
    title: str = Form(...),
    db:Session=Depends(database.get_db)
):
    
    """Create a URL shortener entry."""
    
    msg = []
    
    # authentication
    user = service.get_user_from_token(request, db)
    
    if not user:
        msg.append("Session Expired, Login")
        return templates.TemplateResponse("login.html", {"request": request, "msg": msg})
    
    if not validators.url(target_url):
        msg.append("Invalid destination url, kindly include: https:// or http://")
        return templates.TemplateResponse("create_url.html", 
            {
                "request": request,
                "msg": msg, 
                "user": user, 
                "target_url": target_url,
                "title": title
            }
        )
    
    db_url = crud.create_and_save_url(
        db=db, 
        title=title, 
        url=target_url, 
        user_id = user.id
    )
    db.refresh(db_url)
    return RedirectResponse("/ezzy/dashboard", status_code=status.HTTP_302_FOUND)

#redirect clicks to destination
@router.get("/{url_key}")
async def forward_to_target_url(
    url_key: str, 
    request: Request, 
    db:Session=Depends(database.get_db)
):
    """Forward to the correct full URL."""
    
    if db_url := crud.get_url_by_key(db=db, url_key=url_key):
        crud.update_db_clicks(db=db, db_url=db_url)
        return RedirectResponse(db_url.target_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    else:
        return templates.TemplateResponse("index.html", {"request": request})

#CUSTOMIZE GET ROUTE
@router.get("/customize/{url_key}", response_class=HTMLResponse)
async def customise(
    request: Request, 
    url_key:str, 
    db:Session=Depends(database.get_db)
):
    msg = []
    
    # authentication
    user = service.get_user_from_token(request, db)
    if not user:
        msg.append("session expired, kindly Login")
        return templates.TemplateResponse("login.html", {'request':Request, 'msg':msg})
    
    url_key = db.query(model.URL).filter(model.URL.key == url_key).first()
    
    return templates.TemplateResponse("Customize.html", {"request": request, "user": user, 'url_key': url_key, "msg": msg})


#CUSTOMIZE PUT ROUTE
@router.post("/customize/{url_key}", response_class=HTMLResponse)
async def customize_url_post(
    request: Request,
    url_key:str, 
    custom_name:str = Form(...), 
    title:str = Form(...), 
    target_url:str = Form(...), 
    db:Session=Depends(database.get_db), 
    ):
    
    msg = []
    
    # authentication
    user = service.get_user_from_token(request, db)
    if not user:
        
        msg.append("session expired, kindly Login")
        return templates.TemplateResponse("login.html", {'request':Request, 'msg':msg})
    
    scan_key = db.query(model.URL).filter(model.URL.key == url_key).first()
    if not scan_key:
        return RedirectResponse("/ezzy/dashboard", status_code=status.HTTP_302_FOUND)
    
    availabile = crud.get_url_by_key(url_key=custom_name, db=db)
    
    if availabile:
        
        msg.append("Custom name is taken")
        
        return templates.TemplateResponse(
            "Customize.html", 
            {
                "request": request, 
                'url_key': url_key,
                "msg": msg
            }
        )
    
    scan_key.key = custom_name
    scan_key.title= title
    scan_key.target_url = target_url
    
    db.add(scan_key)
    db.commit()
    db.refresh(scan_key)
    return RedirectResponse("/ezzy/dashboard", status_code=status.HTTP_302_FOUND)


#delete entry routes
@router.get("/delete/{url_key}", response_class=HTMLResponse)
async def delete_url(
    request:Request, 
    url_key: str, 
    db:Session=Depends(database.get_db)
    ):
    
    msg = []
    
    user = service.get_user_from_token(request, db)
    if user is None:
        msg.append("session expired, kindly Login again")
        return templates.TemplateResponse(
            "login.html", 
            {'request':Request, 'msg':msg}, 
            status_code=status.HTTP_403_FORBIDDEN
        )
    
    url_model = db.query(model.URL).filter(model.URL.key == url_key, model.URL.owner_id == user.id).first()
    if url_model is None:
        return RedirectResponse("/ezzy/dashboard", status_code=status.HTTP_302_FOUND)
    
    db.delete(url_model)
    db.commit()
    return RedirectResponse("/ezzy/dashboard", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
