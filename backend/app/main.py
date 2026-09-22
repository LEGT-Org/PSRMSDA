from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.modules.auth.router import router as auth_router
from app.modules.user.router import router as user_router

from app.shared.config import settings

app = FastAPI(title="Server API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.access_control_allowed_origin,
    allow_credentials=settings.allowed_credentials,
    allow_methods=settings.allowed_methods,
    allow_headers=settings.allowed_headers
)


app.include_router(auth_router)
app.include_router(user_router)


@app.get('/')
def home():
    return { 
        'message': 'Server API is running' 
    }