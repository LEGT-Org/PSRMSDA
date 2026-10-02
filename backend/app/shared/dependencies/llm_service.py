from groq import AsyncGroq

from src.shared.llm.groq import GroqLLMProvider
from src.shared.llm.provider import LLMProvider
from src.shared.config import settings


def get_llm_provider() -> LLMProvider:
    
    client = AsyncGroq(
        api_key=settings.groq.api_key,
        timeout=settings.groq.timeout
    )

    return GroqLLMProvider(
        client=client,
        model=settings.groq.model
    )