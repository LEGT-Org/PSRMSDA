from enum import StrEnum


class LLMDiagnosisStatus(StrEnum):

    DRAFT = "Draft"
    ACCEPTED = "Accepted"
    REJECTED = "Rejected"