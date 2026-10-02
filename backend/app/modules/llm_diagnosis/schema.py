from pydantic import BaseModel, Field, field_validator
from enum import StrEnum


class LLMDiagnosisStatus(StrEnum):

    DRAFT = "Draft"
    ACCEPTED = "Accepted"
    REJECTED = "Rejected"


class LLMDiagnosticRequest(BaseModel):
    
    device_type: str
    device_brand: str
    device_model: str
    fault_descriptions: list[str] = Field(
        min_length=3.
        max_length=10
    )


class DiagnosticHypothesis(BaseModel):

    cause: str
    supporting_faults: list[int] = Field(min_length=1)
    reasoning: str
    confidence: Literal[
        "low",
        "moderate",
        "high",
    ]


class DiagnosticStep(BaseModel):

    step: int
    instruction: str
    safety_note: str


class StandardOperatingProcedure(BaseModel):

    title: str
    steps: list[DiagnosticStep]


class ReplacementRecommendation(BaseModel):

    component: str
    reason: str
    compatibility_requirements: list[str]


class LLMDiagnosticResponse(BaseModel):

    summary: str
    diagnostic_hypotheses: list[DiagnosticHypothesis]
    missing_information: list[str]
    recommended_checks: list[str]
    standard_operating_procedure: StandardOperatingProcedure
    replacement_recommendation: ReplacementRecommendation