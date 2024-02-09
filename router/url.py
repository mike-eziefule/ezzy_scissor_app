"""Routes related to URL adding and listing"""

import validators
from fastapi import APIRouter, Depends, HTTPException, status
from schema import url
from sqlalchemy.orm import Session
from storage import database, model
from utils import crud, service
from router.auth import oauth2_scheme
from starlette.datastructures import URL
from config.config import get_settings
from fastapi.responses import RedirectResponse, FileResponse


router = APIRouter(tags=["url"])


#create_url ROUTE
@router.post("/create_short_url", response_model=url.URLListItem)
async def create_url(target_url: str, db:Session=Depends(database.get_db), token:str=Depends(oauth2_scheme)):
    """Create a URL shortener entry."""
    
    # authentication
    user = service.get_user_from_token(db, token)
    
    if not validators.url(target_url):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, 
            detail="URL is not Valid"
        )
    
    db_url = crud.create_and_save_url(db=db, url=target_url, user_id = user.id)
    base_url = URL(get_settings().base_url)
    db_url.url = str(base_url.replace(path = db_url.key))
    
    return db_url

#VIEW URL BY KEY
@router.get("/{url_key}")
async def forward_to_target_url(
    url_key: str,
    db:Session=Depends(database.get_db)
):
    """Forward to the correct full URL."""
    if db_url := crud.get_url_by_key(db=db, url_key=url_key):
        crud.update_db_clicks(db=db, db_url=db_url)
        return RedirectResponse(db_url.target_url)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail= f"NO MATCH FOUND FOR {url_key} KEY"
        )

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
async def download_qr(url_key:str, db:Session=Depends(database.get_db)):
    """download qrcode for website."""
    
    db_url = crud.get_url_by_key(url_key, db)
    
    if not db_url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail= "QR CODE KEY NOT FOUND"
        )
    return FileResponse(
        filename=db_url.key,
        path=db_url.qr_url, 
        media_type="image/png",
        content_disposition_type= "attachment"
    )