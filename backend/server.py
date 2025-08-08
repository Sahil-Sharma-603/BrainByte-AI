# Main Server program for the backend - for running the backend server
# Entry point of backend server

from src.app import app


# basically we can running the app (backend server) using uvicorn - which is a webserver 
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host = "0.0.0.0", port=8000)



