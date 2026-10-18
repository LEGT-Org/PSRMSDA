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


    def get_all(
        self
    ) -> list[Category]:
    
        statement = (
            select(Category)
            .where(Category.parent_category_id.isnot(None))
            .order_by(Category.name.asc())
        )

        return list(self.db.scalars(statement).all())


    def get_all_parent(
        self
    ) -> list[Category]:
    
        statement = (
            select(Category)
            .where(Category.parent_category_id.is_(None))
            .order_by(Category.name.asc())
        )

        return list(self.db.scalars(statement).all())

    
    def get_by_id(
        self,
        category_id: int
    ) -> Category | None:

        statement = select(Category).where(
            Category.id == category_id,
            Category.is_active.is_(True)
        )

        return self.db.scalar(statement)


    def get_parent_by_id(
        self,
        category_id: int
    ) -> Category | None:

        statement = select(Category).where(
            Category.id == category_id,
            Category.parent_category_id.is_(None),
            Category.is_active.is_(True)
        )

        return self.db.scalar(statement)