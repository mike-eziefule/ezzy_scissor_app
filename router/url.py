"""Routes related to URL adding and listing"""

from fastapi import APIRouter, Depends, HTTPException, status


router = APIRouter(prefix="/url", tags=["url"])

#USER REGISTRATION ROUTE
@router.post('/test')
async def test():
    return "url, welcome here"