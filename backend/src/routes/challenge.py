from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database.db import(
    get_challenge_quota,
    create_challenge_quota,
    reset_quota_if_needed,
    create_Challenge,
    get_user_challenge
)

from ..utils import authenticate_and_get_user_details
from ..database.models import get_db
import json
from datetime import datetime

# API Router 
router = APIRouter()


@router.get("/my-history")
async def my_history(request: Request, db: Session = Depends(get_db)):
    user_details = await authenticate_and_get_user_details(request)
    if not user_details:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user_id = user_details.get("user_id")
    challenges = get_user_challenge(db, user_id)
    
    return {"challenges": challenges} 


@router.get("/quota")
async def get_quota(request: Request, db: Session = Depends(get_db)):

    user_details = await authenticate_and_get_user_details(request)
    user_id = user_details.get("user_id")


    quota = get_challenge_quota(db, user_id)
    if not quota:
        return{
            "user_id": user_id,
            "quota_remaining": 0,
            "last_reset_date": datetime.now()
        }
    # Reset the quota if needed
    quota = reset_quota_if_needed(db, quota)
    return quota


