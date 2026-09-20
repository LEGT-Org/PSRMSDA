from typing import Protocol

from app.modules.auth.schema import UserCreate


class UserInterface(Protocol):

    def create_user(self, data: UserCreate):
        pass

    
    def get_user_by_email(self, email: str):
        pass

    
    def get_user_by_id(self, user_id: int):
        pass