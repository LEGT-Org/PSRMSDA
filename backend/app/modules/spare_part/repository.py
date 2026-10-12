from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.spare_part.model import SparePart


class SparePartRepository:
    
    def __init__(self, db: Session):

        self.db = db
    
    def create(
        self, 
        spare_part: SparePart
    ) -> SparePart:

        self.db.add(spare_part)
        return spare_part


    def search_by_name(
        self,
        part_name: str
    ) -> list[SparePart]:

        pattern = f"%{part_name}%"
        statement = select(SparePart).where(SparePart.part_name.ilike(pattern))

        return list(self.db.execute(statement).scalars())


    def get_by_id(
        self,
        part_id: int
    ) -> SparePart:

        statement = select(SparePart).where(SparePart.id == part_id)

        return self.db.scalar(statement)


    def update_quantity(
        self,
        stored_spare_part: SparePart,
        new_quantity: int,
        now: datetime
    ) -> None:

        stored_spare_part.stock_quantity = new_quantity
        stored_spare_part.updated_at = now