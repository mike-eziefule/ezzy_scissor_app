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



#checks availability of user's username and password
def authenticate_user(username: str, password: str, db:database.db_session):
    user = db.query(model.USER).filter(model.USER.email == username).first()
    if not user:
        return False
    if not bcrpyt_context.verify(password, user.password):
        return False
    
    return user

#creates a hex32 token encoding users username. id and expiry time.
def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, get_settings().SECRET_KEY, algorithm=get_settings().ALGORITHM)

#gets user using generated token
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, get_settings().SECRET_KEY, algorithms=[get_settings().ALGORITHM])    
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        return {"email": username, "id": user_id}
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

