from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from .routes import challenge

# new fastapi app
app = FastAPI()

# Add CorsMiddleware 
app.add_middleware(CORSMiddleware, allow_origins=["*"], 
                                   allow_credentials=True, 
                                   allow_methods=["*"],
                                   allow_headers=["*"])


app.include_router(challenge.router, prefix="/api")

