""" carry functions that makes code look bulky"""
from fastapi import Request
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt
from config.config import get_settings
from datetime import timedelta, datetime
from storage import model, database


bcrpyt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_user_from_token(request: Request, db):
    """
        Decode token, extract username/email, 
        then authenticate if user is in db, 
        return user
    """
    try:
        
        token = request.cookies.get('access_token')
        if token is None:
            return None
        
        payload = jwt.decode(token, get_settings().SECRET_KEY, algorithms=[get_settings().ALGORITHM])    
        username: str = payload.get("sub")
        
        #Querry the sub(email) from to token against the stored email
        user = db.query(model.USER).filter(model.USER.email==username).first()        
        if user is None:
            raise None
        
        #if successful, return the user as authenticated, for further processing.
        return user
        
    except Exception as e:
        return False


#checks availability of user's username and password
def authenticate_user(username:str, password: str, expires_delta: timedelta, db:database.db_session):
        
    scan_users = db.query(model.USER).all()

    for row in scan_users:
        
        #authenticate the user
        if row.email == username and bcrpyt_context.verify(password, row.password) == True:
            
            encode = {'sub': username}
            expires = datetime.utcnow() + expires_delta
            encode.update({'exp': expires})
            jwt_token = jwt.encode(encode, get_settings().SECRET_KEY, algorithm=get_settings().ALGORITHM)
            
            return jwt_token
        
    return False
