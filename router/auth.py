"""Routes related to Authentication and Authorization."""
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request, Response, Form
from typing import Annotated
from starlette import status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from storage import database
from schema import user

from storage.database import db_session
from utils import service


router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

templates = Jinja2Templates(directory="templates")



#USER TOKEN GENERATION
@router.post("/token")
async def login_for_access_token(
    response: Response, 
    form_data:Annotated[OAuth2PasswordRequestForm, Depends()], 
    db:db_session):
    
    token = service.authenticate_user(form_data.username, form_data.password, db)
    
    response.set_cookie(key="access_token", value = token, httponly=True)
    
    return True
    # return token

@router.post("/", response_class=HTMLResponse)
async def login(request:Request, db:Session=Depends(database.get_db)):
    
    try:
        form = user.LoginForm(request)
        await form.create_auth_form()
        response = RedirectResponse(url="/ezzy/dashboard", status_code=status.HTTP_302_FOUND)
        
        validate_user_cookie = await login_for_access_token(response=response, form_data=form, db=db)
        
        if not validate_user_cookie:
            msg = "Invalid username or password"
            return templates.TemplateResponse("login.html", {"request": request, "msg": msg})
        return response
    except HTTPException:
        msg = "Unknown error"
        return templates.TemplateResponse("login.html", {"request": request, "msg": msg})
    
