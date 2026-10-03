from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.user.schema import RegistrationStoredUser
from app.modules.user.model import User


class UserRepository:

    def __init__(self, db: Session):

        self.db = db

    
    def create(self, user: User) -> User:

        self.db.add(user)
        return user

    
    def get_by_email(self, email: str) -> User | None:

        statement = select(User).where(
            User.email == email,
            User.is_active.is_(True),
            User.password_hash.isnot(None)
        )

        return self.db.scalar(statement)

    
    def get_by_id(self, user_id: int) -> User | None:

        statement = select(User).where(
            User.id == user_id,
            User.is_active.is_(True),
            User.password_hash.isnot(None)
        )

        return self.db.scalar(statement)
    

    def get_user_by_token_hash(self, hash_token: str) -> User | None:

        statement = select(User).where(
            User.token_hash == hash_token,
            User.email_verified.is_(False),
            User.password_hash.is_(None)    
        )

        return self.db.scalar(statement)

    
    def set_hash_password(
        self, 
        stored_user: RegistrationStoredUser, 
        new_hash_password: str
    ) -> None:

        stored_user.password_hash = new_hash_password
        stored_user.email_verified = True
        stored_user.token_expire = None
        stored_user.token_hash = None

        