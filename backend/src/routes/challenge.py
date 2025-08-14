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

# API Router - allow to create a separate router for challenge related endpoints
router = APIRouter()


# Getting History for the user - GET Request
@router.get("/my-history")
async def my_history(request: Request, db: Session = Depends(get_db)):
    # authenticate the user and get user details
    user_details = await authenticate_and_get_user_details(request)
    if not user_details:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Get user ID from the user details
    user_id = user_details.get("user_id")
    # Get challenges for that user with the user ID
    challenges = get_user_challenge(db, user_id)
    
    return {"challenges": challenges} 



# Getting the challenge quota for the user - GET Request
@router.get("/quota")
async def get_quota(request: Request, db: Session = Depends(get_db)):

    # Authenticate the user and get user details
    user_details = await authenticate_and_get_user_details(request)
    user_id = user_details.get("user_id")

    # get the quota for specfic user from database
    quota = get_challenge_quota(db, user_id)
    # If quota does not exist then there is no quota left for the user
    if not quota:
        return{
            "user_id": user_id,
            "quota_remaining": 0,
            "last_reset_date": datetime.now()
        }
    # Reset the quota if needed
    quota = reset_quota_if_needed(db, quota)
    return quota

# Generate Challenge Request Body
class ChallengeRequest(BaseModel):
    difficulty: str
    
    class Config:
        schema_extra = {
            "example": {
                "difficulty": "easy"
            }
        }
    
# Create Challenge Endpoint - POST Request
@router.post("/create")
async def create_challenge(request:ChallengeRequest, db: Session = Depends(get_db)):
    try:
        user_details = await authenticate_and_get_user_details(request)
        user_id = user_details.get("user_id")

        # Check if the user has enough quota to create a challenge
        quota = get_challenge_quota(db, user_id)
        if not quota:
            quota = create_challenge_quota(db, user_id)
        
        quota = reset_quota_if_needed(db, quota)

        if quota.quota_remaining <= 0:
            raise HTTPException(status_code=429, detail="Challenge quota exceeded for today. Please try again later.")


        challenge_data = None

        quota.quota_remaining -= 1
        db.commit()
        
        return challenge_data

    except Exception as e:
        raise HTTPException(status_code=400, detail="Bad Request 400: " + str(e))



