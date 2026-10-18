from fastapi import status

from app.shared.exception.base import BaseHTTPException


class CategoryDoesNotExistError(BaseHTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Category does not exist"
        )


class InvalidParentCategoryInputError(BaseHTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Invalid selected parent category"
        )


class CategoryCreationFailedError(BaseHTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Add new category has failed"
        )