from typing import Sequence

from app.modules.service_request.model import ServiceRequest
from app.modules.service_request.schema import (
    MatchedSparePartPreview,
    LLMRecommendedSparePart,
    ServiceRequestResponse
)



def build_service_request_response(
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
            llm_recommended_part=None,
            matched_part=[],
            created_at=service_request.created_at,
        )

    llm_recommendation = llm_diagnosis.llm_recommendation

    llm_recommended_part = None

    if llm_recommendation is not None:
        llm_recommended_part = LLMRecommendedSparePart(
            llm_component=llm_recommendation.component,
            llm_reason=llm_recommendation.reason,
            compatibility_requirements=(
                llm_recommendation.compatibility_requirements
            )
        )

    return ServiceRequestResponse(
        service_request_id=service_request.id,
        diagnosis_id=llm_diagnosis.id,
        customer_id=service_request.customer_id,
        status=service_request.status,
        diagnosis=llm_diagnosis.response,
        llm_recommended_part=llm_recommended_part,
        matched_part=matched_parts,
        created_at=service_request.created_at,
    )