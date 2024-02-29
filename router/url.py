"""Routes related to URL adding and listing"""

import validators
from fastapi import APIRouter, Request, Depends, HTTPException, status, Form
from fastapi.responses import HTMLResponse
from schema import url
from sqlalchemy.orm import Session
from storage import database, model
from utils import crud, service
from router.auth import oauth2_scheme
from starlette.datastructures import URL
from config.config import get_settings
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates



router = APIRouter(tags=["url"])


templates = Jinja2Templates(directory="templates")


#VIEW URL BY KEY
@router.get("/", response_class = HTMLResponse)
async def index_page(
    request:Request,
    db:Session=Depends(database.get_db)
):
    return templates.TemplateResponse("index.html", {"request": request})


#create_url GET ROUTE
@router.get("/create_url", response_class=HTMLResponse)
async def create_url(request: Request):
    return templates.TemplateResponse("create_url.html", {"request": request})

#create_url POST ROUTE
@router.post("/create_url", response_class=HTMLResponse)
async def create_url(
    request: Request,
    target_url: str = Form(...),
    title: str = Form(...),
    db:Session=Depends(database.get_db)
):
    
    """Create a URL shortener entry."""
    
    # authentication
    user = service.get_user_from_token(request, db)
    
    if user is None:
        return RedirectResponse("/auth", status_code=status.HTTP_302_FOUND)
    
    if not validators.url(target_url):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, 
            detail="URL is not Valid"
        )
    
    db_url = crud.create_and_save_url(db=db, title=title, url=target_url, user_id = user.id)
    base_url = URL(get_settings().base_url)
    db_url.url = str(base_url.replace(path=db_url.key))
    
    qr = crud.make_qrcode(url_key=db_url.key)
    save_qr =db.query(model.URL).filter(model.URL.key == db_url.key)
    if save_qr.first():
        save_qr.update({"qr_url": qr})
        db.commit()
    
    # msg = "Created successfully"
    return RedirectResponse("ezzy/dashboard", status_code=status.HTTP_302_FOUND)


@router.get("/{url_key}")
async def forward_to_target_url(
    url_key: str, 
    request: Request, 
    db:Session=Depends(database.get_db)
):
    """Forward to the correct full URL."""
    
    if db_url := crud.get_url_by_key(db=db, url_key=url_key):
        crud.update_db_clicks(db=db, db_url=db_url)
        return RedirectResponse(db_url.target_url)
    else:
        return templates.TemplateResponse("index.html", {"request": request})


#CUSTOMIZE GET ROUTE
@router.get("/customise/{url_key}", response_class=HTMLResponse)
async def customise(
    request: Request, 
    url_key:str, 
    db:Session=Depends(database.get_db)
):
    
    # authentication
    user = service.get_user_from_token(request, db)
    
    if user is None:
        return RedirectResponse("/auth", status_code=status.HTTP_403_FORBIDDEN)
    
    url_key = db.query(model.URL).filter(model.URL.key == url_key).first()
    
    return templates.TemplateResponse("customize.html", {"request": request, "user": user, 'url_key': url_key})


#CUSTOMIZE PUT ROUTE
@router.post("/customise/{url_key}", response_class=HTMLResponse)
async def customize_url_entry(
    request: Request,
    url_key:str, 
    custom_name:str = Form(...), 
    title:str = Form(...), 
    target_url:str = Form(...), 
    db:Session=Depends(database.get_db), 
    ):
    
    # authentication
    user = service.get_user_from_token(request, db)
    if user is None:
        return RedirectResponse("/auth", status_code=status.HTTP_302_FOUND)
        
    scan_key = db.query(model.URL).filter(model.URL.key == url_key).first()
    
    
    if crud.get_url_by_key(custom_name, db) == True:
        return RedirectResponse("/auth", status_code=status.HTTP_300_MULTIPLE_CHOICES)
    
    #update qr url
    qr = crud.make_qrcode(url_key= custom_name)
    
    scan_key.key = custom_name
    scan_key.title=title
    scan_key.target_url = target_url
    scan_key.qr_url = qr
    
    db.add(scan_key)
    db.commit()
    return RedirectResponse("/ezzy/dashboard", status_code=status.HTTP_302_FOUND)


#GENERATE QRCODE ROUTE
@router.put("/qrcode/{url_key}")
async def add_qrcode_to_url(url_key:str, db:Session=Depends(database.get_db), token:str=Depends(oauth2_scheme)):
    """Generate qrcode for website, for registered users only"""
    
    # authentication
    user = service.get_user_from_token(db, token)
    
    db_url = crud.get_url_by_key(url_key, db)
    
    if not db_url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail= f"NO MATCH FOUND FOR {url_key} KEY"
        )
    if db_url.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "OWNERS PERMISSION REQUIRED"
        )
        
    if not db_url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail= "URL KEY NOT FOUND"
        )
        
    qr = crud.make_qrcode(url_key = db_url.key)
    save_qr =db.query(model.URL).filter(model.URL.key == url_key)
    if save_qr.first():
        save_qr.update({"qr_url": qr})
        db.commit()
    
    return FileResponse(qr, media_type="image/png")


#DOWNLOAD QR-CODE ROUTE
@router.get("/download/{url_key}")
async def download_qr(
    request: Request,
    url_key:str, 
    db:Session=Depends(database.get_db)
    ):
    
    """download qrcode for website."""
    
    # authentication
    user = service.get_user_from_token(request, db)
    if user is None:
        return RedirectResponse("/auth", status_code=status.HTTP_302_FOUND)
    
    db_url = crud.get_url_by_key(url_key, db)
    
    if not db_url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail= "QR CODE KEY NOT FOUND"
        )
        
    return FileResponse(
        filename=db_url.key+".png",
        path=db_url.qr_url, 
        media_type="image/png",
        content_disposition_type= "attachment"
    )
    
    
@router.get("/delete/{url_key}", response_class=HTMLResponse)
async def delete_todo(
    request:Request, 
    url_key: str, 
    db:Session=Depends(database.get_db)
    ):
    
    user = service.get_user_from_token(request, db)
    
    if user is None:
        return RedirectResponse("/auth", status_code=status.HTTP_302_FOUND)
    
    url_model = db.query(model.URL).filter(model.URL.key == url_key, model.URL.owner_id == user.id).first()
    
    if url_model is None:
        return RedirectResponse("/ezzy/dashboard", status_code=status.HTTP_302_FOUND)
    
    db.delete(url_model)
    db.commit()
    
    return RedirectResponse("/ezzy/dashboard", status_code=status.HTTP_302_FOUND)