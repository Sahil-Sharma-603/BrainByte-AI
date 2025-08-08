from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware


# new fastapi app
app = FastAPI()

# Add CorsMiddleware 
app.add_middleware(CorsMiddleware, allow_origins=["*"], 
                                   allow_credentials=True, 
                                   allow_methods=["*"],
                                   allow_headers=["*"])


