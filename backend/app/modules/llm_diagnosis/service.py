from sqlalchemy.orm import Session

from app.shared.config import settings
from app.shared.value_object.llm_diagnostic import (
    LLMDiagnosticResponse as LLMResponseValidation,
    LLMDiagnosticRequest as LLMRequestValidation
)

from app.shared.infrastructure.llm import (
    DiagnosticPromptBuilder,
    LLMProvider
)

from app.modules.llm_diagnosis.repository import LLMDiagnosisRepository
from app.modules.llm_diagnosis.model import LLMDiagnosis
from app.modules.llm_diagnosis.schema import (
    LLMDiagnosticResponse,
    LLMDiagnosticRequest,
    LLMDiagnosisStatus
)


class LLMDiagnosisService:
    
    def __init__(
        self,
        repository: LLMDiagnosisRepository,
        prompt_builder: DiagnosticPromptBuilder,
        llm_service: LLMProvider,
        db: Session
    ):

        self.repository = repository
        self.prompt_builder = prompt_builder
        self.llm_service = llm_service
        self.db = db

    
    async def analyze(
        self,
        service_request_id: int | None = None,
        request: LLMDiagnosticRequest
    ) -> LLMDiagnosticResponse:

        user_request = LLMRequestValidation(
            device_type=request.device_type,
            device_brand=request.device_brand,
            device_model=request.device_model,
            fault_descriptions=request.fault_descriptions
        )

        system_prompt = (self.prompt_builder.build_system_prompt())
        
        user_prompt = (
            self.prompt_builder.build_user_prompt(
                device_type=user_request.validated_device_type,
                device_brand=user_request.validated_device_brand,
                device_model=user_request.validated_device_model,
                fault_descriptions=user_request.validated_fault_descriptions
            )
        )

        raw_output = await self.llm_service.analyze(
            system_prompt=system_prompt,
            user_prompt=user_prompt
        )

        llm_response = LLMResponseValidation(
            response=raw_output,
            fault_count=len(user_request.validated_fault_descriptions)
        )

        parsed_output = llm_response.validated_response

        llm_diagnosis = LLMDiagnosis(
            model=settings.groq.model
            prompt=user_prompt,
            raw_output=raw_output,
            summary=parsed_output.summary,
            confidence=self._overall_confidence(parsed_ output),
            parsed_output=parsed_output.model_dump(mode="json"),
            status=LLMDiagnosisStatus.DRAFT
            request_id=service_request_id
        )

        return llm_diagnosis


    def stage(
        self,
        diagnosis: LLMDiagnosis
    ) -> LLMDiagnosis:

        self.repository.create(diagnosis)
        self.db.flush()

        return diagnosis