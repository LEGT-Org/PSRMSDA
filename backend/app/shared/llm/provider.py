from typing import Protocol


class LLMProvider(Protocol):

    def analyze(
        self,
        system_prompt: str,
        user_prompt: str
    ) -> str:

        pass