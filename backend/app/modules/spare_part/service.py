from sqlalchemy.orm import Session

from app.modules.spare_part.repository import SparePartRepository
from app.modules.spare_part.interface import CategoryInterface
from app.modules.spare_part.model import SparePart


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