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

from ..utlis import authenticate_and_get_user_details
from ..database.models import get_db
import json
from datetime import datetime
from ..ai_generator import generate_challenge_with_ai

# API Router - allow to create a separate router for challenge related endpoints
router = APIRouter()


# Getting History for the user - GET Request
@router.get("/my-history")
async def my_history(request: Request, db: Session = Depends(get_db)):
    # authenticate the user and get user details
    user_details = authenticate_and_get_user_details(request)
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
    user_details = authenticate_and_get_user_details(request)
    user_id = user_details.get("user_id")

    # Get the quota for specific user from database
    quota = get_challenge_quota(db, user_id)
    
    # If quota does not exist, create it
    if not quota:
        quota = create_challenge_quota(db, user_id)
    
    # Reset the quota if needed
    quota = reset_quota_if_needed(db, quota)
    
    # Return as dict for consistency (though FastAPI serializes the model fine)
    return {
        "user_id": quota.user_id,
        "quota_remaining": quota.quota_remaining,
        "last_reset_date": quota.last_reset_date.isoformat()
    }



# Generate Challenge Request Body
class ChallengeRequest(BaseModel):
    difficulty: str
    category: str

    class Config:
        schema_extra = {
            "example": {"difficulty": "easy", "category": "Vocabulary"}
        }

CATEGORIES = [
    "Working Memory",
    "Vocabulary",
    "Grammar",
    "Applied Math",
    "Police Logic",
    "Problem Solving",
    "Map Navigation",
    "Reading Comprehension",
]

@router.post("/create")
async def create_challenge(request: ChallengeRequest, request_obj: Request, db: Session = Depends(get_db)):
    try:
        user_details = authenticate_and_get_user_details(request_obj)
        if not user_details:
            raise HTTPException(status_code=401, detail="Unauthorized")
        user_id = user_details.get("user_id")

        # pull category from request and validate
        category = request.category
        if category not in CATEGORIES:
            raise HTTPException(status_code=422, detail=f"Invalid category: {category}")

        # quota
        quota = get_challenge_quota(db, user_id) or create_challenge_quota(db, user_id)
        quota = reset_quota_if_needed(db, quota)
        if quota.quota_remaining <= 0:
            raise HTTPException(status_code=429, detail="Challenge quota exceeded for today. Please try again later.")

        # generate with AI (use request.difficulty and the validated category)
        challenge_data = generate_challenge_with_ai(request.difficulty, category)

        # persist (make sure your create_Challenge signature includes category)
        new_challenge = create_Challenge(
            db=db,
            difficulty=request.difficulty,
            category=category,
            created_by=user_id,
            title=challenge_data['title'],
            options=json.dumps(challenge_data['options']),
            correct_answer_id=challenge_data['correct_answer_id'],
            explanation=challenge_data['explanation']
        )

        quota.quota_remaining -= 1
        db.commit()

        return {
            "id": new_challenge.id,
            "difficulty": request.difficulty,
            "category": category,
            "title": new_challenge.title,
            "options": json.loads(new_challenge.options),
            "correct_answer_id": new_challenge.correct_answer_id,
            "explanation": new_challenge.explanation,
            "timestamp": new_challenge.date_created.isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        # Surface the real reason to the client for easier debugging
        raise HTTPException(status_code=400, detail=f"Bad Request 400: {e}")



# # Generate Challenge Request Body
# class ChallengeRequest(BaseModel):


#     difficulty: str
#     category: str
    
#     class Config:
#         schema_extra = {
#             "example": {
#                 "difficulty": "easy",
#                 "category": "Vocabulary"
#             }
#         }

# CATEGORIES = [
#     "Working Memory",
#     "Vocabulary",
#     "Grammar",
#     "Applied Math",
#     "Police Logic",
#     "Problem Solving",
#     "Map Navigation",
#     "Reading Comprehension",
# ]

# #Create Challenge Endpoint - POST Request
# @router.post("/create")
# async def create_challenge(request:ChallengeRequest, request_obj: Request, db: Session = Depends(get_db)):
#     try:
#         user_details = authenticate_and_get_user_details(request_obj)
#         user_id = user_details.get("user_id")

#         # Check if the user has enough quota to create a challenge
#         quota = get_challenge_quota(db, user_id)
#         if not quota:
#             quota = create_challenge_quota(db, user_id)
        
#         quota = reset_quota_if_needed(db, quota)

#         if quota.quota_remaining <= 0:
#             raise HTTPException(status_code=429, detail="Challenge quota exceeded for today. Please try again later.")


#         challenge_data = generate_challenge_with_ai(request.difficulty,category)

#         # Now we have the challenfge data, we can create a challenge in the database
#         new_challenge = create_Challenge(
#             db=db,
#             difficulty=request.difficulty,
#             category=category,
#             created_by=user_id,
#             title = challenge_data['title'],
#             options=json.dumps(challenge_data['options']),
#             correct_answer_id=challenge_data['correct_answer_id'],
#             explanation=challenge_data['explanation']   
#         )

#         quota.quota_remaining -= 1
#         db.commit()
        
#         return {
#             "id": new_challenge.id,
#             "difficulty": request.difficulty,
#             "category": category,
#             "title": new_challenge.title,
#             "options": json.loads(new_challenge.options),
#             "correct_answer_id": new_challenge.correct_answer_id,
#             "explanation": new_challenge.explanation,
#             "timestamp": new_challenge.date_created.isoformat()
#         }

#     except Exception as e:
#         raise HTTPException(status_code=400, detail="Bad Request 400: " + str(e))

