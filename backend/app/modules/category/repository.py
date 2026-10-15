from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.category.model import Category


class CategoryRepository:

    def __init__(self, db: Session):

        self.db = db

    def create(
        self,
        category: Category
    ) -> Category:

        self.db.add(category)
        return category

    
    def get_by_id(
        self,
        category_id: int
    ) -> Category | None:

        statement = select(Category).where(
            Category.id == category_id,
            Category.is_active.is_(True)
        )

        return self.db.scalar(statement)