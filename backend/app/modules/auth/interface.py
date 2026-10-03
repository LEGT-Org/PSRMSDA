from typing import Protocol

from app.modules.user.model import User

class UserInterface(Protocol):
    
    def get_user_by_email(
        self, 
        email: str
    ) -> User:
        
        pass

    
    def get_user_by_id(
        self, 
        user_id: int
    ) -> User:

        pass


    def set_user_new_password(
        self, 
        token_hash: str, 
        new_password: str
    ) -> User:
    
        pass