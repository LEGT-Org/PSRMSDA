from sqlalchemy.orm import Session

from app.modules.request_part.repository import RequestPartRepository


class RequestPartService:

    def __init__(
        self,
        repository: RequestPartRepository,
        db: Session
    ):

        self.repository = repository
        self.db = db