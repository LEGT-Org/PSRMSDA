from typing import Protocol

from app.modules.llm_diagnosis.schema import (
    LLMDiagnosticResponse,
    LLMDiagnosticRequest
)

from app.modules.customer.schema import (
    CustomerResponse,
    CustomerRequest
)


class LLMDiagnosisInterface(Protocol):

    async def analyze(
        self,
        request: LLMDiagnosticRequest
    ) -> LLMDiagnosticResponse:

        pass


class CustomerInterface(Protocol):

    def find_or_create_customer(
        self,
        customer_request: CustomerRequest
    ) -> CustomerResponse:

        pass