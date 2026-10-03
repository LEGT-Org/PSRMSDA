from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.request_part.model import RequestPart


class RequestPartRepository:
    
    def __init__(self, db: Session):

        self.db = db
    
    def create(
        self, 
        request_part: RequestPart
    ) -> RequestPart:

        self.db.add(request_part)
        return request_part