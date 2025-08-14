# Main backend authentication Setup - 
# where JWT token sent by the frontend is processed and verifies
# Frontend will send JWT and there are two ways to verify the JWT token
# 1) Sending request to Clerk Server to verify the JWT token
# 2) is using JWT Public key to verify the JWT token - this is used when Clerk Server is not available and has zero latency (faster)


from clerk_backend_api import Clerk,  AuthenticateRequestOptions
from dotenv import load_dotenv
import os
from fastapi import HTTPException

# This will Load environment variables from .env file
load_dotenv()


clerk_sdk = Clerk(bearer_auth=os.getenv('CLERK_SECRET_KEY'))

# Request Authentication function - frontend will send the JWT token in the request header
# this function will check if the JWT token is valid or not.
def authenticate_and_get_user_details(request):
    try:
        request_state = clerk_sdk.autenticate_request(request
        ,AuthenticateRequestOptions(
            authorized_parties=['http://localhost:5173/'],
            jwt_key = os.getenv('JWT_KEY')
        ))

        if not request_state.is_signed_in:
            raise HTTPException(status_code=401, detail="Invalid JWT Token")
    
        # If the JWT token is valid, we can get the user details from the request state
        # This will help to determine which user is making the request
        user_id = request_state.payload.get('sub')

        return {"user_id": user_id}

    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized: " + str(e))

