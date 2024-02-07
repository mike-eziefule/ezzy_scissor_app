from storage.database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship


class USER(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index = True)
    username = Column(String, nullable= False)
    email = Column(String, nullable= False, unique=True)
    password = Column(String, nullable= False, index= True)    
    
    urls = relationship("URL", back_populates = "owner")


class URL(Base):
    __tablename__ = 'urls'
    
    id = Column(Integer, primary_key=True, index = True)
    target_url = Column(String, nullable= False)
    key = Column(String, nullable= False, unique=True)
    private_key = Column(String, nullable= False, unique=True)
    clicks = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    date_created = Column(Date, nullable= False)
    qr_url = Column(String, nullable= True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("USER", back_populates = "urls")