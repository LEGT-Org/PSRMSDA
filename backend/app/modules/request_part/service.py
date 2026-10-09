from sqlalchemy.orm import Session

from app.shared.exception import RequestPartFailedError

from app.modules.request_part.repository import RequestPartRepository
from app.modules.request_part.schema import RequestPartSchema
from app.modules.request_part.model import RequestPart


class RequestPartService:

    def __init__(
        self,
        repository: RequestPartRepository,
        db: Session
    ):

        self.repository = repository
        self.db = db


    def create_request(
        self,
        data: RequestPartSchema
    ) -> RequestPart:

        request_part = RequestPart(
            request_id=data.request_id,
            part_id=data.part_id,
            quantity=data.quantity,
            part_name_snapshot=data.part_name_snapshot,
            is_stock_validated=data.is_stock_validated
        )
        
        try:

            self.repository.create(request_part)
            self.db.flush()

            return request_part

        except Exception as error:
            
            self.db.rollback()
            raise RequestPartFailedError() from error