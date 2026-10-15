from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from slowapi import _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded

from app.shared.rate_limiter import limiter
from app.shared.config import settings

# Models Configuration

from app.modules.procurement_alert.model import ProcurementAlert
from app.modules.service_request.model import ServiceRequest
from app.modules.llm_diagnosis.model import LLMDiagnosis
from app.modules.request_part.model import RequestPart
from app.modules.spare_part.model import SparePart
from app.modules.customer.model import Customer
from app.modules.category.model import Category
from app.modules.auth.model import RefreshToken
from app.modules.user.model import User   

# Router Configuration

from app.modules.procurement_alert.router import router as procurement_alert_router
from app.modules.service_request.router import router as service_request_router
from app.modules.spare_part.router import router as spare_part_router
from app.modules.customer.router import router as customer_router
from app.modules.auth.router import router as auth_router
from app.modules.user.router import router as user_router


app = FastAPI(title="Server API",)


app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded, 
    _rate_limit_exceeded_handler,
)


app.add_middleware(SlowAPIMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors.access_control_allowed_origin,
    allow_credentials=settings.cors.allowed_credentials,
    allow_methods=settings.cors.allowed_methods,
    allow_headers=settings.cors.allowed_headers
)


app.include_router(procurement_alert_router)
app.include_router(service_request_router)
app.include_router(spare_part_router)
app.include_router(customer_router)
app.include_router(user_router)
app.include_router(auth_router)


@app.get('/')
def home():

    return { 
        'message': 'Server API is running' 
    }