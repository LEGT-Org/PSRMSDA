from datetime import (
    datetime,
    timedelta,
    timezone
)

from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.modules.user.repository import UserRepository
from app.modules.user.value_object.email import Email
from app.modules.user.value_object.name import Name
from app.modules.user.schema import UserRole
from app.modules.user.model import User

from app.shared.exception import (
    EmailAlreadyExistsError, 
    InvalidCredentialsError
)


class UserService:

    def __init__(
        self,
        repository: UserRepository,
        db: Session
    ):

        self.repository = repository
        self.db = db

    
    def create_user(
        self,
        first_name: str,
        last_name: str,
        email: EmailStr,
        password_hash: str
    ) -> User:

        Name(first_name)
        Name(last_name)
        Email(email)

        if self.repository.get_by_email(email):
            raise EmailAlreadyExistsError()

        now = datetime.now(timezone.utc)
        
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password_hash=password_hash,
            role=UserRole.USER,
            created_at=now,
            updated_at=now,
            deleted_at=None
        )

        self.repository.create(user)

        self.db.commit()
        self.db.refresh(user)

        return user


    def get_user_by_email(
        self, 
        email: EmailStr
    ) -> User:

        Email(email)

        user = self.repository.get_by_email(email)

        if user is None:
            raise InvalidCredentialsError()

        return user


    def get_user_by_id(
        self,
        user_id: int
    ) -> User:

        user = self.repository.get_by_id(user_id)

        return user