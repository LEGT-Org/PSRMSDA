from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.modules.spare_part.repository import SparePartRepository
from app.modules.spare_part.interface import CategoryInterface
from app.modules.spare_part.model import SparePart

from app.shared.exception import (
    SparePartInsufficientQuantityError,
    SparePartUpdateQuantityError
)


class SparePartService:
    
    def __init__(
        self,
        repository: SparePartRepository,
        category_interface: CategoryInterface,
        db: Session
    ):

        self.repository = repository
        self.category_interface = category_interface
        self.db = db


    def search_matched_spare_part(
        self,
        part_name: str
    ) -> list[SparePart]:

        spare_part = self.repository.search_by_name(part_name)

        return spare_part


    def get_spare_part_by_id(
        self,
        part_id: int
    ) -> SparePart:

        spare_part = self.repository.get_by_id(part_id)

        return spare_part


    def deduct_spare_part_quantity(
        self,
        part_id: int,
        quantity_used: int
    ) -> int:

        now = datetime.now(timezone.utc).replace(tzinfo=None)
        stored_spare_part = self.repository.get_by_id(part_id)
        new_quantity = stored_spare_part.stock_quantity - quantity_used

        if new_quantity < 0:
            raise SparePartInsufficientQuantityError()

        try:

            self.repository.update_quantity(
                stored_spare_part=stored_spare_part,
                new_quantity=new_quantity,
                now=now
            )

            self.db.flush()

            return new_quantity

        except Exception as error:
            
            raise SparePartUpdateQuantityError() from error


    def add_spare_part_quantity(
        self,
        part_id: int,
        quantity_to_add: int
    ) -> int:

        now = datetime.now(timezone.utc).replace(tzinfo=None)
        stored_spare_part = self.repository.get_by_id(part_id)
        new_quantity = stored_spare_part.stock_quantity + quantity_to_add

        if new_quantity < 0:
            raise SparePartInsufficientQuantityError()

        try:

            self.repository.update_quantity(
                stored_spare_part=stored_spare_part,
                new_quantity=new_quantity,
                now=now
            )

            self.db.flush()

            return new_quantity

        except Exception as error:
            
            raise SparePartUpdateQuantityError() from error