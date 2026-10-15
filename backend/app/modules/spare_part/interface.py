from typing import Protocol

from app.modules.category.model import Category


class CategoryInterface(Protocol):

    def get_category_by_id(
        self,
        category_id: str
    ) -> Category:

        pass