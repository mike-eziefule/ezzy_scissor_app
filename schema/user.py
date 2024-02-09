""" schema validation for user route"""
from pydantic import EmailStr, BaseModel


class BaseUser(BaseModel):
    email : EmailStr
    
class UserLogin(BaseUser):
    username : str
    
class UserCreate(UserLogin):
    password: str
    
class editUser(BaseModel):
    username: str
    
class ShowUser(UserLogin):
    id : int
    
    class Config:
        orm_mode = True