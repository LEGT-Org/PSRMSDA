from typing import Sequence

from app.modules.service_request.model import ServiceRequest
from app.modules.service_request.schema import (
    MatchedSparePartPreview,
    ServiceRequestResponse
)



def build_service_request_response(
    self, 
    service_request: ServiceRequest,
    matched_parts: Sequence[MatchedSparePartPreview] | list = []
) -> ServiceRequestResponse:
    
    llm_diagnosis = service_request.llm_diagnosis

    if llm_diagnosis is None:
        return ServiceRequestResponse(
            service_request_id=service_request.id,
            diagnosis_id=None,
            customer_id=service_request.customer_id,
            status=service_request.status,
            diagnosis=None,
            confidence=None,
            model=None,
            llm_recommended_part=None,
            matched_part=[],
            created_at=service_request.created_at,
        )

    return ServiceRequestResponse(
        service_request_id=service_request.id,
        diagnosis_id=llm_diagnosis.id,
        customer_id=service_request.customer_id,
        status=service_request.status,
        diagnosis=llm_diagnosis.response,
        confidence=llm_diagnosis.confidence,
        model=llm_diagnosis.model,
        llm_recommended_part=llm_recommendation,
        matched_part=matched_parts,
        created_at=service_request.created_at,
    )