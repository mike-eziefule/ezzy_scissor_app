"""Main FastAPI App."""
from fastapi import FastAPI
from storage.database import engine
from router import auth, url, user
from storage.model import Base
from config.config import get_settings


app = FastAPI(
    title="Ezzy Scissor application",
    description="A FastAPI-based URL shortener and redirector.",
    version="0.1.0",
    openapi_tags= get_settings().tags
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(url.router)