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