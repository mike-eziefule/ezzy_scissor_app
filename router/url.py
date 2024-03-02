"""Routes related to URL adding and listing"""

import validators
from fastapi import APIRouter, Request, Depends, status, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from storage import database, model
from utils import crud, service
from starlette.datastructures import URL
from config.config import get_settings
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates


router = APIRouter(tags=["url"])


templates = Jinja2Templates(directory="templates")


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
    
    # authentication
    user = service.get_user_from_token(request, db)
    if not user:
        msg = []
        
        msg.append("Session Expired, Login")
        return templates.TemplateResponse("login.html", {"request": request, "msg": msg})
    
    if not validators.url(target_url):
        return RedirectResponse("/ezzy/dashboard", status_code=status.HTTP_307_TEMPORARY_REDIRECT)

    
    db_url = crud.create_and_save_url(
        db=db, 
        title=title, 
        url=target_url, 
        user_id = user.id
    )
    
    base_url = URL(get_settings().base_url)
    db_url.url = str(base_url.replace(path=db_url.key))
    
    #generare qr image
    #remind me to put this in try/except block
    qr = crud.make_qrcode(url_key=db_url.key)
    
    #save qr image path to db file
    save_qr =db.query(model.URL).filter(model.URL.key == db_url.key)
    if save_qr.first():
        save_qr.update({"qr_url": qr})
        db.commit()
    
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
@router.get("/customise/{url_key}", response_class=HTMLResponse)
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
    
    return templates.TemplateResponse("customize.html", {"request": request, "user": user, 'url_key': url_key})


#CUSTOMIZE PUT ROUTE
@router.post("/customise/{url_key}", response_class=HTMLResponse)
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
    
    check_availabile = crud.get_url_by_key(url_key=custom_name, db=db)
    
    if check_availabile:
        
        msg.append("Custom name is taken")
        return templates.TemplateResponse(
            "customize.html", 
            {"request": request, 
                'url_key': scan_key,
                "msg": msg
            }
        )
    
    #update qr image
    qr = crud.make_qrcode(url_key= custom_name)
    
    scan_key.key = custom_name
    scan_key.title= title
    scan_key.target_url = target_url
    scan_key.qr_url = qr
    
    db.add(scan_key)
    db.commit()
    db.refresh(scan_key)
    return RedirectResponse("/ezzy/dashboard", status_code=status.HTTP_302_FOUND)


#DOWNLOAD QR-CODE ROUTE
@router.get("/download/{url_key}")
async def download_qr(
    request: Request,
    url_key:str, 
    db:Session=Depends(database.get_db)
    ):
    
    """download qrcode for website."""
    msg = []
    
    # authentication
    user = service.get_user_from_token(request, db)
    if user is None:
        msg.append("session expired, kindly Login again")
        return templates.TemplateResponse("login.html", {'request':Request, 'msg':msg}, status_code=status.HTTP_403_FORBIDDEN)
    
    db_url = crud.get_url_by_key(url_key, db)
    if not db_url:
        # msg.append("URL does not exist")
        return RedirectResponse("/ezzy/dashboard", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    
    return FileResponse(
        filename=db_url.key+".png",
        path=db_url.qr_url, 
        media_type="image/png",
        content_disposition_type= "attachment"
    )

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
