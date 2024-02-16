"""Routes related to User Account creation."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schema import user
from storage import database
from storage import model
from utils.service import bcrpyt_context, get_user_from_token
from router.auth import oauth2_scheme


router = APIRouter(prefix="/user", tags=["user"])

#NEW USER REGISTRATION
@router.post('/sign-up', response_model = user.ShowUser)
async def register(new_user:user.UserCreate, db:Session=Depends(database.get_db)):
    
    scan = db.query(model.USER).filter(model.USER.email == new_user.email)
    if scan.first():
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, 
            detail="email already registered"
        )
    
    new_user = model.USER(
        username=new_user.username,
        email=new_user.email,
        password = bcrpyt_context.hash(new_user.password),
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


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
