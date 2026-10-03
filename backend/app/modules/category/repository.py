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