from datetime import datetime
from typing import Literal

from sqlalchemy import select, func, or_
from sqlalchemy.orm import Session

from app.modules.user.schema import RegistrationStoredUser, UserRole
from app.modules.user.model import User


class UserRepository:

    def __init__(self, db: Session):

        self.db = db

    
    def create(self, user: User) -> User:

        self.db.add(user)
        return user


    def get_all(
        self,
        page: int,
        limit: int,
        search: str | None = None,
        role: UserRole | None = None,
        status: Literal["active", "disabled"] | None = None,
    ) -> tuple[list[User], int]:

        statement = select(User).where(
            User.deleted_at.is_(None)
        )

        if search and search.strip():
            search_value = f"%{search.strip()}%"

            statement = statement.where(
                or_(
                    User.first_name.ilike(search_value),
                    User.last_name.ilike(search_value),
                    User.email.ilike(search_value),
                )
            )

        if role is not None:
            statement = statement.where(User.role == role)

        if status == "active":
            statement = statement.where(User.is_active.is_(True))

        elif status == "disabled":
            statement = statement.where(User.is_active.is_(False))

        count_statement = (
            select(func.count())
            .select_from(statement.subquery())
        )
        
        total = self.db.scalar(count_statement) or 0

        statement = (
            statement
            .offset((page - 1) * limit)
            .limit(limit)
        )

        users = list(self.db.scalars(statement).all())

        return users, total
    

    def get_by_email(self, email: str) -> User | None:

        statement = select(User).where(
            User.email == email,
            User.is_active.is_(True),
            User.deleted_at.is_(None),
            User.password_hash.isnot(None)
        )

        return self.db.scalar(statement)

    
    def get_by_id(self, user_id: int) -> User | None:

        statement = select(User).where(
            User.id == user_id,
            User.password_hash.isnot(None),
            User.deleted_at.is_(None)
        )

        return self.db.scalar(statement)


    def get_user_by_token_hash(self, hash_token: str) -> User | None:

        statement = select(User).where(
            User.token_hash == hash_token,
            User.email_verified.is_(False),
            User.password_hash.is_(None),    
            User.deleted_at.is_(None)
        )

        return self.db.scalar(statement)


    def get_by_id_for_soft_deletion(
        self,
        user_id: int    
    ) -> User | None:

        statement = select(User).where(
            User.id == user_id,
            User.deleted_at.is_(None)
        )

        return self.db.scalar(statement)


    def count_active_users(
        self
    ) -> int:

        statement = (
            select(func.count())
            .select_from(User)
            .where(
                User.deleted_at.is_(None),
                User.email_verified.is_(True),
                User.is_active.is_(True),
            )
        )

        return self.db.scalar(statement) or 0

    
    def set_hash_password(
        self, 
        stored_user: RegistrationStoredUser, 
        new_hash_password: str
    ) -> None:

        stored_user.password_hash = new_hash_password
        stored_user.email_verified = True
        stored_user.token_expire = None
        stored_user.token_hash = None
        stored_user.is_active = True


    def set_token_hash(
        self,
        stored_user: RegistrationStoredUser,
        token_expire: datetime,
        token_hash: str
    ) -> None:

        stored_user.token_expire = token_expire
        stored_user.token_hash = token_hash
        stored_user.email_verified = False
        stored_user.password_hash = None
        stored_user.is_active = False

    
    def enable(
        self,
        stored_user: User,
        approve_by: int,
        now: datetime
    ) -> None:

        stored_user.last_modified_by_id = approve_by
        stored_user.is_active = True
        stored_user.updated_at = now


    def disable(
        self,
        stored_user: User,
        approve_by: int,
        now: datetime
    ) -> None:

        stored_user.last_modified_by_id = approve_by
        stored_user.is_active = False
        stored_user.updated_at = now


    def promote(
        self,
        stored_user: User,
        approve_by: int,
        now: datetime
    ) -> None:

        stored_user.last_modified_by_id = approve_by
        stored_user.role = UserRole.ADMIN
        stored_user.updated_at = now


    def demote(
        self,
        stored_user: User,
        approve_by: int,
        now: datetime
    ) -> None:

        stored_user.last_modified_by_id = approve_by
        stored_user.role = UserRole.USER
        stored_user.updated_at = now

    
    def delete(
        self,
        stored_user: User,
        approve_by: int,
        now: datetime
    ) -> None:

        stored_user.password_hash = None
        stored_user.token_expire = None
        stored_user.token_hash = None
        stored_user.is_active = False
        stored_user.email = None

        stored_user.last_modified_by_id = approve_by
        stored_user.updated_at = now
        stored_user.deleted_at = now




        