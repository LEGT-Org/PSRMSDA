from datetime import datetime

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, selectinload

from app.modules.spare_part.model import SparePart
from app.modules.category.model import Category


class SparePartRepository:
    
    def __init__(self, db: Session):

        self.db = db
    
    def create(
        self, 
        spare_part: SparePart
    ) -> SparePart:

        self.db.add(spare_part)
        self.db.flush()
        
        return spare_part


    def search_by_name(
        self,
        part_name: str,
        device_type: str
    ) -> list[SparePart]:

        pattern = f"%{part_name}%"

        statement = (
            select(SparePart)
            .join(SparePart.categories)
            .where(
                SparePart.part_name.ilike(pattern),
                Category.name.ilike(device_type)
            )
        )

        return list(self.db.execute(statement).scalars().all())


    def get_all(
        self,
        page: int,
        limit: int,
        search: str | None = None,
        category_id: int | None = None,
        parent_category_id: int | None = None,
    ) -> tuple[list[SparePart], int]:

        statement = (
            select(SparePart)
            .where(SparePart.deleted_at.is_(None))
        )

        if search:
            search_value = f"%{search.strip()}%"

            statement = (
                statement
                .join(SparePart.categories)
                .where(
                    or_(
                        SparePart.part_name.ilike(search_value),
                        SparePart.part_code.ilike(search_value),
                        SparePart.device_model.ilike(search_value),
                        SparePart.device_brand.ilike(search_value),
                        SparePart.specifications.ilike(search_value),
                        SparePart.shelf_location.ilike(search_value),
                        Category.name.ilike(search_value),
                    )
                )
            )

        if category_id is not None:
            statement = statement.where(
                SparePart.category_id == category_id
            )

        if parent_category_id is not None:
            statement = statement.where(
                SparePart.categories.has(
                    Category.parent_category_id == parent_category_id
                )
            )

        count_statement = (
            select(func.count())
            .select_from(statement.subquery())
        )

        total = self.db.scalar(count_statement) or 0

        statement = (
            statement
            .options(selectinload(SparePart.categories))
            .order_by(SparePart.created_at.desc())
            .offset((page - 1) * limit)
            .limit(limit)
        )

        spare_parts = list(self.db.scalars(statement).all())

        return spare_parts, total


    def get_by_id(
        self, 
        spare_part_id: int
    ) -> SparePart | None:

        statement = (
            select(SparePart)
            .options(selectinload(SparePart.categories))
            .where(
                SparePart.id == spare_part_id,
                SparePart.deleted_at.is_(None),
            )
        )

        return self.db.scalar(statement)


    def get_by_part_code(
        self, 
        part_code: str
    ) -> SparePart | None:

        statement = select(SparePart).where(
            SparePart.part_code == part_code,
            SparePart.deleted_at.is_(None),
        )

        return self.db.scalar(statement)


    def update(
        self,
        stored_spare_part: SparePart,
        category_id: int,
        approve_by: int,
        updates: dict,
        now: datetime
    ) -> SparePart:

        for field, value in updates.items():
            setattr(stored_spare_part, field, value)

        if "category_id" in updates:
            stored_spare_part.category_id = category_id

        stored_spare_part.last_modified_by_id = approve_by
        stored_spare_part.updated_at = now

        return stored_spare_part


    def update_quantity(
        self,
        stored_spare_part: SparePart,
        new_quantity: int,
        now: datetime
    ) -> None:

        stored_spare_part.stock_quantity = new_quantity
        stored_spare_part.updated_at = now


    def delete(
        self,
        stored_spare_part: SparePart,
        approve_by: int,
        now: datetime,
    ) -> SparePart:

        stored_spare_part.last_modified_by_id = approve_by
        stored_spare_part.updated_at = now
        stored_spare_part.deleted_at = now

        return stored_spare_part