from fastapi import FastAPI

from app.modules.auth.router import router as auth_router

app = FastAPI(title="Server API")


app.include_router(auth_router)


@app.get('/')
def home():
    return { 
        'message': 'Server API is running' 
    }