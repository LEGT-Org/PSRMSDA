from enum import StrEnum
from datetime import datetime
from decimal import Decimal

from pydantic import (
    BaseModel, 
    EmailStr,
    Field
)

from app.modules.llm_diagnosis.schema import LLMDiagnosticResponse, LLMDiagnosisStatus

class ServiceRequestStatus(StrEnum):

    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    FOR_FURTHER_INSPECTION = "For Further Inspection"
    UNSUCCESSFUL = "Unsuccessful"


class SelectedPart(BaseModel):
    
    part_id: int | None = None          
    part_name: str                       
    quantity: int = Field(ge=1, default=1)


class ConfirmServiceRequest(BaseModel):

    selected_parts: list[SelectedPart] = Field(default_factory=list)
    final_status: ServiceRequestStatus
    diagnosis_verdict: LLMDiagnosisStatus = LLMDiagnosisStatus.ACCEPTED
    technician_notes: str | None = None


class LLMRecommendedSparePart(BaseModel):

    llm_component: str
    llm_reason: str | None = None
    compatibility_requirements: list[str] = Field(
        default_factory=list
    )


class MatchedSparePartPreview(BaseModel):

    part_id: int
    part_name: str
    part_code: str
    device_model: str | None = None
    device_brand: str | None = None
    specifications: str | None = None
    unit_cost: Decimal | None = None
    stock_quality: int | None = None
    shelf_location: str
    image_url: str | None = None
    category_id: int
    is_available: bool


class ServiceRequestResponse(BaseModel):

    service_request_id: int
    diagnosis_id: int
    customer_id: int
    status: ServiceRequestStatus
    diagnosis: LLMDiagnosticResponse
    llm_recommended_part: LLMRecommendedSparePart | None = None 
    matched_part: list[MatchedSparePartPreview] = []
    created_at: datetime


class LLMDiagnosticRequestPreview(BaseModel):
    
    device_type: str
    device_brand: str
    device_model: str
    fault_descriptions: list[str] = Field(
        min_length=3,
        max_length=10
    )


class CustomerRequestPreview(BaseModel):

    first_name: str = Field(
        min_length=2,
        max_length=50
    )

    last_name: str = Field(
        min_length=2,
        max_length=50
    )

    email: EmailStr
    phone_number: str


class UserSchema(BaseModel):

    id: int
    first_name: str
    last_name: str
    email: str
    role: str
