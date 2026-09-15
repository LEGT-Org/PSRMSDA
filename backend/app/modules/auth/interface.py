from typing import Protocol

from app.modules.auth.schema import UserCreate


class UserInterface(Protocol):

    def create_user(self, data: UserCreate):
        pass