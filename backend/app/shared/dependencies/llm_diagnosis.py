from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.shared.session import get_db
from app.shared.dependencies.external_service.llm_service import (
    get_llm_provider,
    get_llm_builder
)

from app.shared.infrastructure.llm import (
    DiagnosticPromptBuilder,
    LLMProvider
) 

from app.modules.llm_diagnosis.repository import LLMDiagnosisRepository
from app.modules.llm_diagnosis.service import LLMDiagnosisService


def get_llm_diagnosis_repository(
    db: Annotated[
        Session,
        Depends(get_db)
    ]
) -> LLMDiagnosisRepository:

    return LLMDiagnosisRepository(db)


def get_llm_diagnosis_service(
    repository: Annotated[
        LLMDiagnosisService,
        Depends(get_llm_diagnosis_repository)
    ],
    prompt_builder: Annotated[
        DiagnosticPromptBuilder,
        Depends(get_llm_builder)
    ],
    llm_service: Annotated[
        LLMProvider,
        Depends(get_llm_provider)
    ],
    db: Annotated[
        Session,
        Depends(get_db)
    ]
) -> LLMDiagnosisService:

    return LLMDiagnosisService(
        repository=repository,
        prompt_builder=prompt_builder,
        llm_service=llm_service,
        db=db
    )
