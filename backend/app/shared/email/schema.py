from pydantic import BaseModel


class EmailServiceSchema(BaseModel):

    to: str
    subject: str
    body: str
    html: str | None = None