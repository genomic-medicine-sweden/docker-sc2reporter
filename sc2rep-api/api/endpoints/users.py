
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from starlette.responses import JSONResponse

from db import *
from authentication import *

router = APIRouter()


@router.get("/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.get("/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user['username']}]