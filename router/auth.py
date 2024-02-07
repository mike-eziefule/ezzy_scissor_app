"""Routes related to Authentication and Authorization."""

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from storage.database import db_session
from utils import service
from datetime import timedelta


router = APIRouter(prefix="/auth", tags=["auth"])


#USER REGISTRATION ROUTE
@router.post("/token")
async def retrieve_token_after_authentication(response:Response, form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:db_session):

    user = service.authenticate_user(form_data.username, form_data.password, db)
    
    if not user:
        return False
    
    token = service.create_access_token(user.username, user.id, timedelta(minutes=60))
    
    response.set_cookie(key="access_token", value = token, httponly=True)
    
    # return True
    return token


    # for row in user:
    #     if row.email == form_data.username and row.password == form_data.password:
    #         data = {'sub': form_data.username}
    #         jwt_token = jwt.encode(data, setting.SECRET_KEY, algorithm=setting.ALGORITHM)
    #         return {"access_token": jwt_token, "token_type": "bearer"}
        
    # raise HTTPException(
    #     status_code=status.HTTP_401_UNAUTHORIZED, 
    #     detail="invalid credentials"
    #     )