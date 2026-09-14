from fastapi import FastAPI

from app.shared.dependencies import get_db

app = FastAPI(title="Server API")


@app.get('/')
def home():
    return { 
        'message': 'Server API is running' 
    }