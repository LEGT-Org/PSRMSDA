from sqlalchemy.orm import Session

from app.modules.spare_part.repository import SparePartRepository


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