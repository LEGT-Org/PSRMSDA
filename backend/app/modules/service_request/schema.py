from enum import StrEnum
from datetime import datetime
from decimal import Decimal

from pydantic import (
    BaseModel, 
    EmailStr,
    Field
)

from app.modules.procurement_alert.schema import ProcurementAlertType
from app.modules.request_part.schema import RequestPartUsage
from app.modules.user.schema import UserRole
from app.modules.llm_diagnosis.schema import (
    StandardOperatingProcedure,
    LLMDiagnosticResponse, 
    LLMDiagnosisStatus
) 

class ServiceRequestStatus(StrEnum):

    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    FOR_FURTHER_INSPECTION = "For Further Inspection"
    UNSUCCESSFUL = "Unsuccessful"


class ProcurementAlertTypePreview(StrEnum):

    FINALIZED_REQUEST = ProcurementAlertType.FINALIZED_REQUEST
    REQUEST_STAGE = ProcurementAlertType.REQUEST_STAGE
    PART_SELECTED = ProcurementAlertType.PART_SELECTED
    NO_PART_MATCH = ProcurementAlertType.NO_PART_MATCH
    PART_NOT_FOUND = ProcurementAlertType.PART_NOT_FOUND
    INSUFFICIENT_STOCK = ProcurementAlertType.INSUFFICIENT_STOCK


class UserRolePreview(StrEnum):

    USER = UserRole.USER
    ADMIN = UserRole.ADMIN


class LLMDiagnosisStatusPreview(StrEnum):

    DRAFT = LLMDiagnosisStatus.DRAFT
    ACCEPTED = LLMDiagnosisStatus.ACCEPTED
    REJECTED = LLMDiagnosisStatus.REJECTED


class ServiceRequestStatusUpdate(BaseModel):

    status: ServiceRequestStatus


class SelectedPart(BaseModel):
    
    part_id: int | None = None          
    part_name: str                       
    quantity: int = Field(ge=1, default=1)


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


class ConfirmServiceRequest(BaseModel):

    service_request_id: int | None = None

    customer_data: CustomerRequestPreview
    device_type: str
    device_brand: str
    device_model: str
    fault_descriptions: list[str]

    selected_parts: list[SelectedPart] = Field(default_factory=list)
    final_status: ServiceRequestStatus
    technician_notes: str | None = None
    diagnosis_verdict: LLMDiagnosisStatusPreview | None = None


class CancelServiceRequest(BaseModel):

    service_request_id: int


class LLMRecommendedSparePart(BaseModel):

    llm_component: str
    llm_reason: str | None = None
    compatibility_requirements: list[str] = Field(default_factory=list)


class MatchedSparePartPreview(BaseModel):

    part_id: int
    part_name: str
    part_code: str

    device_model: str | None = None
    device_brand: str | None = None
    specifications: str | None = None

    unit_cost: Decimal | None = None
    stock_quantity: int | None = None
    shelf_location: str

    image_url: str | None = None
    category_name: str
    is_available: bool


class ServiceRequestResponse(BaseModel):

    service_request_id: int
    diagnosis_id: int | None = None
    customer_id: int
    status: ServiceRequestStatus
    diagnosis: LLMDiagnosticResponse | None = None
    llm_recommended_part: LLMRecommendedSparePart | None = None 
    matched_parts: list[MatchedSparePartPreview] = []
    created_at: datetime


class LLMDiagnosticRequestPreview(BaseModel):
    
    device_type: str
    device_brand: str
    device_model: str
    fault_descriptions: list[str] = Field(
        min_length=3,
        max_length=10
    )


class UserSchema(BaseModel):

    id: int
    first_name: str
    last_name: str
    email: str
    role: str


class ProcurementAlertRequest(BaseModel):

    request_id: int
    part_id: int | None = None
    part_name_snapshot: str | None = None
    is_resolved: bool = False
    created_at: datetime
    alert_type: ProcurementAlertType
    alert_message: str | None = None


class RequestPartRequest(BaseModel):

    request_id: int
    part_id: int
    quantity: int | None = None
    quantity_used: int | None = None
    part_name_snapshot: str
    is_stock_validated: bool = False
    part_used: bool | None = None

class ServiceRequestListResponse(BaseModel):

    id: int
    customer_name: str
    technician_name: str
    device_type: str
    device_brand: str
    device_model: str
    created_at: datetime
    status: ServiceRequestStatus


class ServiceRequestPageListResponse(BaseModel):

    items: list[ServiceRequestListResponse]
    page: int
    limit: int
    total: int
    pages: int


class UserServiceRequestDetails (BaseModel):

    id: int
    name: str


class CustomerServiceRequestDetails (BaseModel):

    id: int
    name: str


class RequestPartDetails (BaseModel):

    id: int
    quantity: int
    part_name: str
    validated: bool


class ServiceRequestDetailsResponse(BaseModel):

    id: int
    device_type: str
    device_brand: str
    device_model: str
    fault_descriptions: list[str]
    technician_notes: str | None = None
    status: ServiceRequestStatus
    diagnosis: LLMDiagnosticResponse | None = None
    customer: CustomerServiceRequestDetails
    technician: UserServiceRequestDetails
    requested_part: list[RequestPartDetails]


class ServiceRequestFinalizeRequest(BaseModel):

    status: ServiceRequestStatus
    parts_usage: list[RequestPartUsage]