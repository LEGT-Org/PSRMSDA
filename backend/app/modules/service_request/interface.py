from typing import Protocol

from app.modules.procurement_alert.model import ProcurementAlert
from app.modules.llm_diagnosis.model import LLMDiagnosis
from app.modules.request_part.model import RequestPart
from app.modules.spare_part.model import SparePart

from app.modules.procurement_alert.schema import ProcurementAlertSchema
from app.modules.request_part.schema import RequestPartSchema
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
        request: LLMDiagnosticRequest,
        service_request_id: int | None = None
    ) -> LLMDiagnosticResponse:

        pass

    def stage(
        self,
        diagnosis: LLMDiagnosis
    ) -> LLMDiagnosis:

        pass


class CustomerInterface(Protocol):

    def find_or_create_customer(
        self,
        customer_request: CustomerRequest
    ) -> CustomerResponse:

        pass


class ProcurementAlertInterface(Protocol):

    def create_procurement_alert(
        self,
        data: ProcurementAlertSchema
    ) -> ProcurementAlert:

        pass

    def cancel_by_request(
        self,
        part_id: int,
        alert_message: str
    ) -> ProcurementAlert:

        pass


class SparePartInterface(Protocol):

    def search_matched_spare_part(
        self,
        part_name: str,
        device_type: str
    ) -> list[SparePart]:

        pass

    def get_spare_part_specific_details(
        self,
        part_id: int
    ) -> SparePart:

        pass

    def deduct_spare_part_quantity(
        self,
        part_id: int,
        quantity_used: int
    ) -> None:

        pass

    def add_spare_part_quantity(
        self,
        part_id: int,
        quantity_to_add: int
    ) -> None:

        pass


class RequestPartInterface(Protocol):

    def create_request(
        self,
        data: RequestPartSchema
    ) -> RequestPart:

        pass

