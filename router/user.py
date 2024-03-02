"""Routes related to User Account creation."""

from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from storage import database, model
from utils.service import bcrpyt_context
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter(prefix="/user", tags=["user"])

templates = Jinja2Templates(directory="templates")


#register page route
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
    
    msg = []
    
    if password != password2:
        msg.append("Passwords do not match")
        return templates.TemplateResponse("register.html", {
            "request": request, 
            "msg": msg,
            'email': email,
            "firstname": firstname,  
            "lastname": lastname
        })
    
    if len(password) < 6:
        msg.append("Password should be > 6 character")
        return templates.TemplateResponse("register.html", {
            "request": request, 
            "msg": msg,
            'email': email,
            "firstname": firstname,  
            "lastname": lastname
        })

    new_user = model.USER(
        firstname = firstname,
        lastname = lastname,
        email = email,
        password = bcrpyt_context.hash(password),
    )
    
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        msg.append("Registration successful")
        return templates.TemplateResponse(
            "login.html", 
            {"request": request, 
                "msg": msg,
            })
        
    except IntegrityError:
        msg.append("Email already taken")
        return templates.TemplateResponse("register.html", {
            "request": request, 
            "msg": msg,
            'email': email,
            "firstname": firstname,  
            "lastname": lastname
        })


# #EDITING USER INFORMATION BY User ONLY
# @router.put("/edit_user")
# async def edit_username(username, db:Session=Depends(database.get_db), token:str=Depends(oauth2_scheme)):
    
#     # authentication
#     user = get_user_from_token(db, token)
    
#     #Authorazation
#     scan_db = db.query(model.USER).filter(model.USER.email == user.email)
#     if not scan_db.first():
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, 
#             detail="UNAUTHORIZED USER"
#         )
    
#     scan_db.update({model.USER.username:username})
#     db.commit()
#     raise HTTPException(
#             status_code=status.HTTP_202_ACCEPTED, 
#             detail='Information updated successfully'
#         )
