from sqlalchemy.orm import Session

from app.modules.category.repository import CategoryRepository
from app.modules.category.model import Category
from app.modules.category.schema import (
    CategoryResponse,
    CategoryRequest,
    ParentCategory,
    ChildCategory,
)

from app.shared.exception import (
    InvalidParentCategoryInputError,
    CategoryCreationFailedError,
    CategoryDoesNotExistError,
) 


class CategoryService:

    def __init__(
        self,
        repository: CategoryRepository,
        db: Session
    ):

        self.repository = repository
        self.db = db


    def create_new_category(
        self,
        request: CategoryRequest
    ) -> Category:

        parent_category = self.repository.get_parent_by_id(
            request.parent_category_id
        )

        if parent_category is None:
            InvalidParentCategoryInputError()

        category = Category(
            name=request.name,
            description=request.description,
            parent_category_id=request.parent_category_id,
            is_active=True
        )

        try:
            
            self.repository.create(category)

            self.db.commit()
            self.db.refresh(category)

            return category

        except Exception as error:

            self.db.rollback()
            raise CategoryCreationFailedError()


    def get_list_of_categories(
        self
    ) -> list[CategoryResponse]:

        parent_categories = self.repository.get_all_parent()
        categories = self.repository.get_all()

        child_items = [
            ChildCategory(
                id=category.id,
                name=category.name,
                parent_category_id=category.parent_category_id
            )
            for category in categories
        ]

        parent_items = [
            ParentCategory(
                id=parent.id,
                name=parent.name
            )
            for parent in parent_categories
        ]

        return CategoryResponse(
            category=child_items,
            parent=parent_items
        )
    
    def get_category_by_id(
        self,
        category_id: int
    ) -> Category:

        category = self.repository.get_by_id(category_id)

        if category is None:
            raise CategoryDoesNotExistError()

        return category