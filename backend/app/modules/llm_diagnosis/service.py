from app.shared.llm.builder import DiagnosticPromptBuilder
from app.shared.llm.provider import LLMProvider
from app.shared.value_object.llm_diagnostic import (
    LLMDiagnosticResponse as LLMResponseValidation,
    LLMDiagnosticRequest as LLMRequestValidation
)

from app.modules.llm_diagnosis.schema import (
    LLMDiagnosticResponse,
    LLMDiagnosticRequest
)


class DiagnosticService:
    
    def __init__(
        self,
        prompt_builder: DiagnosticPromptBuilder,
        llm_service: LLMProvider
    ):

        self.prompt_builder = prompt_builder
        self.llm_service = llm_service

    
    async def analyze(
        self,
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

        response = await self.llm_service.analyze(
            system_prompt=system_prompt,
            user_prompt=user_prompt
        )

        llm_response = LLMResponseValidation(
            response=response,
            fault_count=len(user_request.validated_fault_descriptions)
        )

        return response