from fastapi import FastAPI

app = FastAPI(title="Server API")


@app.get('/')
def home():
    return { 
        'message': 'Server API is running' 
    }