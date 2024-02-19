"""Routes related to User Account creation."""

from fastapi import APIRouter, Depends, HTTPException, Request, Response, Form
from sqlalchemy.orm import Session
from schema import user
from storage import database
from storage import model
from utils.service import bcrpyt_context, get_user_from_token
from router.auth import oauth2_scheme
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates




router = APIRouter(prefix="/user", tags=["user"])
templates = Jinja2Templates(directory="templates")



#GET NEW USER REGISTRATION
@router.get("/sign-up", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

#NEW USER REGISTRATION
@router.post('/sign-up', response_class=HTMLResponse)
async def register(
    request: Request, 
    email: str = Form(...), 
    firstname: str = Form(...), 
    lastname: str = Form(...), 
    password: str = Form(...), 
    password2: str = Form(...),
    db:Session=Depends(database.get_db)
    ):
    
    scan_for_existing = db.query(model.USER).filter(model.USER.email == email).first()
    
    if scan_for_existing is not None:
        msg = "Email Already registered"
        return templates.TemplateResponse("register.html", {"request": request, "msg": msg})
    
    if password != password2:
        msg = "Passwords do not match"
        return templates.TemplateResponse("register.html", {"request": request, "msg": msg})
    
    
    new_user = model.USER(
        firstname = firstname,
        lastname = lastname,
        email = email,
        password = bcrpyt_context.hash(password),
    )
    
    db.add(new_user)
    db.commit()
    
    msg = "Registered successfully"
    return templates.TemplateResponse("login.html", {"request": request, "msg": msg})
    

#EDITING USER INFORMATION BY User ONLY
@router.put("/edit_user")
async def edit_username(username, db:Session=Depends(database.get_db), token:str=Depends(oauth2_scheme)):
    
    # authentication
    user = get_user_from_token(db, token)
    
    #Authorazation
    scan_db = db.query(model.USER).filter(model.USER.email == user.email)
    if not scan_db.first():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="UNAUTHORIZED USER"
        )
    
    scan_db.update({model.USER.username:username})
    db.commit()
    raise HTTPException(
            status_code=status.HTTP_202_ACCEPTED, 
            detail='Information updated successfully'
        )
