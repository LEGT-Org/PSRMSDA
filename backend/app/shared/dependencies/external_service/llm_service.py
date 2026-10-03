from groq import AsyncGroq

from app.shared.config import settings
from app.shared.infrastructure.llm import (
    DiagnosticPromptBuilder,
    GroqLLMProvider,
    LLMProvider
)


def get_llm_builder() -> DiagnosticPromptBuilder:
    return DiagnosticPromptBuilder()


def get_llm_provider() -> LLMProvider:
    
    client = AsyncGroq(
        api_key=settings.groq.api_key,
        timeout=settings.groq.timeout
    )

    return GroqLLMProvider(
        client=client,
        model=settings.groq.model
    )