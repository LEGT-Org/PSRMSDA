from pydantic import BaseModel, ConfigDict


class CategoryRequest(BaseModel):

    parent_category_id: int
    name: str
    description: str
    

class ParentCategory(BaseModel):

    id: int
    name: str


class ChildCategory(BaseModel):

    id: int
    name: str
    parent_category_id: int


class CategoryResponse(BaseModel):

    category: list[ChildCategory]
    parent: list[ParentCategory]