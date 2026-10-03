from sqlalchemy.orm import Session

from app.modules.category.repository import CategoryRepository


class CategoryService:

    def __init__(
        self,
        repository: CategoryRepository,
        db: Session
    ):

        self.repository = repository
        self.db = db