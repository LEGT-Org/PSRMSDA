from typing import Literal, NamedTuple
from enum import StrEnum
from pydantic import (
    ConfigDict,
    BaseModel, 
    Field,  
    field_validator
)


class LLMDiagnosisStatus(StrEnum):

    DRAFT = "Draft"
    ACCEPTED = "Accepted"
    REJECTED = "Rejected"


class LLMDiagnosticRequest(BaseModel):
    
    device_type: str
    device_brand: str
    device_model: str
    fault_descriptions: list[str] = Field(
        min_length=3,
        max_length=10
    )


class DiagnosticHypothesis(BaseModel):

    model_config = ConfigDict(extra="forbid")

    cause: str
    supporting_faults: list[int] = Field(min_length=1)
    reasoning: str
    confidence: Literal[
        "low",
        "moderate",
        "high",
    ]


class DiagnosticStep(BaseModel):

    model_config = ConfigDict(extra="forbid")

    step: int
    instruction: str
    safety_note: str


class StandardOperatingProcedure(BaseModel):

    model_config = ConfigDict(extra="forbid")

    title: str
    steps: list[DiagnosticStep]


class ReplacementRecommendation(BaseModel):

    model_config = ConfigDict(extra="forbid")

    component: str
    reason: str
    compatibility_requirements: list[str]


class LLMDiagnosticResponse(BaseModel):

    model_config = ConfigDict(extra="forbid")

    summary: str
    llm_model: str
    diagnostic_hypotheses: list[DiagnosticHypothesis]
    missing_information: list[str]
    recommended_checks: list[str]
    standard_operating_procedure: StandardOperatingProcedure
    replacement_recommendation: ReplacementRecommendation
    overall_confidence: Literal[
        "low",
        "moderate",
        "high",
    ]


class LLMServiceResult(NamedTuple):

    raw: str
    parsed: LLMDiagnosticResponse