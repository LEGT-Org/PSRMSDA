from sqlalchemy.orm import Session

from app.shared.exception import CategoryDoesNotExistError

from app.modules.category.repository import CategoryRepository
from app.modules.category.model import Category


class CategoryService:

    def __init__(
        self,
        repository: CategoryRepository,
        db: Session
    ):

        self.repository = repository
        self.db = db

    
    def get_category_by_id(
        self,
        category_id: int
    ) -> Category:

        category = self.repository.get_by_id(category_id)

        if category is None:
            raise CategoryDoesNotExistError()

        return category