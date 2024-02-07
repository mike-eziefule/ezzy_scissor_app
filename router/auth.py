"""Routes related to Authentication and Authorization."""

from fastapi import APIRouter, Depends, HTTPException, Request, Response


router = APIRouter(prefix="/auth", tags=["auth"])


#USER REGISTRATION ROUTE
@router.post('/test')
async def register_user():
    return "auth, welcome here"