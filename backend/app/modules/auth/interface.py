from typing import Protocol


class UserInterface(Protocol):
    
    def get_user_by_email(self, email: str):
        pass

    
    def get_user_by_id(self, user_id: int):
        pass


    def set_user_new_password(self, token_hash: str, new_password: str):
        pass