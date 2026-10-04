import groq
from groq import AsyncGroq

from app.modules.llm_diagnosis.schema import LLMDiagnosticResponse, LLMServiceResult

from app.shared.infrastructure.llm.provider import LLMProvider
from app.shared.exception import (
    LLMServiceAuthenticationError,
    LLMServiceUnavailableError,
    LLMServiceRateLimitError,
    LLMServiceContentError,
    LLMServiceTimeoutError
)



class GroqLLMProvider:
    
    def __init__(
        self,
        client: AsyncGroq,
        model: str
    ) -> None:

        self.client = client
        self.model = model

    
    async def analyze(
        self,
        system_prompt: str,
        user_prompt: str
    ) -> LLMServiceResult:

        try:
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "diagnostic_response",
                        "schema": LLMDiagnosticResponse.model_json_schema(),
                        "strict": True,
                    },
                },
            )
            
            content = response.choices[0].message.content

            if not content:
                raise LLMServiceContentError()

            parsed = LLMDiagnosticResponse.model_validate_json(content)

            return LLMServiceResult(
                raw=content,
                parsed=parsed
            )

        except groq.AuthenticationError as exc:
            raise LLMServiceAuthenticationError() from exc

        except groq.RateLimitError as exc:
            raise LLMServiceRateLimitError() from exc

        except groq.APITimeoutError as exc:
            raise LLMServiceTimeoutError() from exc

        except groq.InternalServerError as exc:
            raise LLMServiceUnavailableError() from exc

