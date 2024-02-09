""" carry functions that makes code look bulky"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import jwt, JWTError

from config.config import get_settings
from datetime import timedelta, datetime
from storage import model, database
from typing import Annotated


bcrpyt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_user_from_token(db, token):
    
    """
    Decode token,extract username/email, 
    then authenticate if user is in db, return user
    
    """
    try:
        
        payload = jwt.decode(token, get_settings().SECRET_KEY, algorithms=[get_settings().ALGORITHM])    
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Invalid Email credentials"
            )
            
        #Querry the sub(email) from to token against the stored email
        user = db.query(model.USER).filter(model.USER.email==username).first()        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="User is not authorized"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Unable to verify credentials"
        )
    
    #if successful, return the user as authenticated, for further processing.
    return user


#checks availability of user's username and password
def authenticate_user(username:str, password: str, db:database.db_session):
    
    scan_users = db.query(model.USER).all()
    expires_delta = timedelta(minutes=60)

    for row in scan_users:
        
        #authenticate the user
        if row.email == username and bcrpyt_context.verify(password, row.password) == True:
            
            data = {'sub': username}
            # expires = datetime.utcnow() + expires_delta
            # encode.update({'exp': expires})
            jwt_token = jwt.encode(data, get_settings().SECRET_KEY, algorithm=get_settings().ALGORITHM)
            return {"access_token": jwt_token, "token_type": "bearer"}
        
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Email and/or password is incorrect"
    )
