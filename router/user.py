"""Routes related to User Account creation."""

from fastapi import APIRouter, Depends, HTTPException, status



router = APIRouter(prefix="/user", tags=["user"])

#USER REGISTRATION ROUTE
@router.post('/test')
async def test():
    return "user, welcome here"
