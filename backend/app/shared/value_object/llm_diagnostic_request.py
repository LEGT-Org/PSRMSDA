from dataclasses import dataclass

from app.shared.exception import (
    LLMDiagnosisInvalidListOfStringError, 
    LLMDiagnosisInvalidStringError
)


@dataclass(frozen=True)
class LLMDiagnosticRequest:

    device_type: str
    device_brand: str
    device_model: str
    fault_descriptions: list[str]


    def __post_init__(self):

        self._validate_string_text(device_type)
        self._validate_string_text(device_brand)
        self._validate_string_text(device_model)
        self._validate_list_of_string(fault_descriptions)

    
    @staticmethod
    def _validate_string_text(value: str) -> None:

        value = value.strip()

        if not value:
            raise LLMDiagnosisInvalidStringError()

    @staticmethod
    def _validate_list_of_string(value: list[str]) -> None:

        cleaned_faults = [
            fault.strip()
            for fault in value
        ]

        if any(not fault for fault in cleaned_faults):
            raise LLMDiagnosisInvalidListOfStringError()
    
    @property
    def validated_device_type(self) -> str:
        return self.device_type

    @property
    def validated_device_brand(self) -> str:
        return self.device_brand

    @property
    def validated_device_model(self) -> str:
        return self.device_model

    @property
    def validated_fault_descriptions(self) -> list[str]:
        return self.fault_descriptions