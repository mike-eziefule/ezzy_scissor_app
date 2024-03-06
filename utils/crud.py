"""CRUD operations."""

from config.config import get_settings
from starlette.datastructures import URL
from schema import url
from utils import keygen, qrcode
from storage import model
from sqlalchemy.orm import Session
from datetime import datetime
import tempfile

img_path = "static/images/qr_images/"
base_url = URL(get_settings().base_url)



def create_and_save_url(db, title, url, user_id) -> url.URL:
    
    """Create URL in the Database."""
    #generate unique key
    key = keygen.create_unique_random_key(db)

    #database dump
    db_url = model.URL(
        title = title,
        target_url= url,
        key= key,
        date_created = datetime.now().date(), 
        owner_id = user_id
    )
    db.add(db_url)
    db.commit()
    return db_url

#function 2
def get_url_by_key(url_key:str, db:Session) -> model.URL:
    """Return a URL by specified key."""
    
    return (
        db.query(model.URL)
        .filter(model.URL.key == url_key)
        .first()
    )


def update_db_clicks(db: Session, db_url: model.URL) -> model.URL:
    """Update the count of times the link has been visited."""
    db_url.clicks += 1
    db.commit()
    db.refresh(db_url)
    return db_url    



def make_qrcode(url_key):
    
    tempfile.tempdir = img_path

    shorturl = str(base_url.replace(path = url_key))
    # Create qr_code
    qrcode.qr_image().url_to_qr(
        url=shorturl, 
        img_path= tempfile.tempdir, 
        url_key=url_key
    )

    return (img_path+url_key+'.png')