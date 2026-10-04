from typing import Protocol

from app.modules.category.model import Category


class CategoryInterface(Protocol):

    def get_category_by_name(
        self,
        category_name: str
    ) -> Category:

        pass