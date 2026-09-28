from dataclasses import dataclass

from app.shared.exception import (
    EmailMustContainBodyOrHTML,
    RecipientIsRequiredError,
    SubjectIsRequiredError
)

@dataclass(frozen=True)
class EmailMessage:

    to: str
    subject: str
    body: str
    html: str | None = None


    def __post_init__(self):

        self._validate_message(
            to=self.to,
            subject=self.subject,
            body=self.body,
            html=self.html
        )
        

    @staticmethod
    def _validate_message(
        to: str,
        subject: str,
        body: str,
        html: str | None = None
    ) -> None:
        
        if not to:
            raise RecipientIsRequiredError()

        if not subject:
            raise SubjectIsRequiredError()

        if not body and not html:
            raise EmailMustContainBodyOrHTML()


    @property
    def validated_to(self) -> str:
        return self.to

    @property
    def validated_subject(self) -> str:
        return self.subject

    @property
    def validated_body(self) -> str:
        return self.body

    @property
    def validated_html(self) -> str | None:
        return self.html

        