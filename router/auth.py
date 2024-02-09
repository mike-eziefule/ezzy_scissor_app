"""Routes related to Authentication and Authorization."""

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from storage.database import db_session
from utils import service
from datetime import timedelta


router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


#USER REGISTRATION ROUTE
@router.post("/token")
async def login_for_access_token(form_data:Annotated[OAuth2PasswordRequestForm, Depends()], db:db_session):

    token = service.authenticate_user(form_data.username, form_data.password, db)
    
    # response.set_cookie(key="access_token", value = token, httponly=True)
    
    # return True
    return token
