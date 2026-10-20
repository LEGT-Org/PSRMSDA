from typing import Literal
from math import ceil
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session

from app.modules.user.schema import UserRole, UserCreate, UserPageListResponse
from app.modules.user.repository import UserRepository
from app.modules.user.model import User

from app.shared.config import settings
from app.shared.infrastructure.email import (
    JinjaEmailRendered,
    EmailService, 
    EmailMessage
)

from app.shared.value_object.user import (
    Email as EmailValidation,
    User as UserValidation
)

from app.shared.security.password import (
    generate_registration_token,
    hash_registration_token,
    hash_password
)

from app.shared.exception import (
    InvalidRegistrationTokenError,
    InsufficientPermissionsError,
    InvalidEmailAddressError,
    EmailAlreadyExistsError, 
    InvalidCredentialsError,
    EmailServiceFailedError,
    SetupNewPasswordError   
)


class UserService:

    def __init__(
        self,
        repository: UserRepository,
        email_service: EmailService,
        email_renderer: JinjaEmailRendered,
        db: Session
    ):

        self.repository = repository
        self.email_service = email_service
        self.email_renderer = email_renderer
        self.db = db

    
    def create_user(
        self,
        actor_id: int,
        data: UserCreate
    ) -> User:

        try:

            validate_user = UserValidation(
                first_name=data.first_name,
                last_name=data.last_name,
            )

            validate_email = EmailValidation(email=data.email)

            if self.repository.get_by_email(validate_email.validated_email):
                raise EmailAlreadyExistsError()

            now = datetime.now(timezone.utc).replace(tzinfo=None)

            raw_token = generate_registration_token()
            token_hash = hash_registration_token(raw_token)
            token_expire = now + timedelta(hours=settings.auth.password_setup_token_expire_hours)
            
            user = User(
                first_name=validate_user.validated_first_name,
                last_name=validate_user.validated_last_name,
                email=validate_email.validated_email,
                password_hash=None,
                role=UserRole.USER,
                token_hash=token_hash,
                token_expire=token_expire,
                email_verified=False,
                is_active=False,
                created_at=now,
                updated_at=now,
                deleted_at=None,
                last_modified_by_id=actor_id
            )

            self.repository.create(user)

            action_url = (
                f"{settings.frontend.url}/password/set"
                f"?token={raw_token}"
            )

            html = self.email_renderer.render(
                "set_your_password.html",

                title="Set Your Password",
                preheader="Set your password to activate your account.",
                company_name="Lightyear Electrical Goods Trading",
                address="60 Burgos Street, Brgy. 3, Calamba City, 4027, Laguna, Philippines",
                first_name=user.first_name,
                last_name=user.last_name,
                first_intro="An account has been created for you on Lightyear Electrical Goods Trading  by LEGT team.",
                second_intro="To get started, simply set your password by clicking the button below.",
                button="SET MY PASSWORD",
                invite_link=action_url,
                exp_notice="This link expires in 72 hours.",
                ending="If you weren't expecting this invitation, you can safely ignore this email — no account will be activated without your action.",
                regards="Welcome aboard,",
                team="The LEGT team",
                footer_text="Need help? Contact us at ",
                footer_link="legt@gmail.com"
            )

            message = EmailMessage(
                to=user.email,
                subject="Welcome to PSRMSDA",
                body=(f"Your account has been successfully created.\n\n"
                    "Please set your password using the link below."
                ),
                html=html
            )

            self.email_service.send(message)

            self.db.commit()
            self.db.refresh(user)

            return user

        except EmailAlreadyExistsError:

            self.db.rollback()
            raise

        except Exception as error:

            self.db.rollback()
            raise EmailServiceFailedError() from error


    def password_reset(
        self,
        email: str
    ) -> None:

        try:

            email = EmailValidation(email=email)
            user = self.repository.get_by_email(email.validated_email)

            if user is None:
                raise InvalidEmailAddressError()

            if user.email_verified is False:
                raise InvalidEmailAddressError()

            now = datetime.now(timezone.utc).replace(tzinfo=None)

            raw_token = generate_registration_token()
            token_hash = hash_registration_token(raw_token)
            token_expire = now + timedelta(hours=settings.auth.password_reset_token_expire_hours)

            self.repository.set_token_hash(
                stored_user=user,
                token_expire=token_expire,
                token_hash=token_hash
            )

            action_url = (
                f"{settings.frontend.url}/password/set"
                f"?token={raw_token}"
            )

            html = self.email_renderer.render(
                "reset_password.html",

                preheader="Reset password to activate your account.",
                company_name="Lightyear Electrical Goods Trading",
                address="60 Burgos Street, Brgy. 3, Calamba City, 4027, Laguna, Philippines",
                first_name=user.first_name,
                last_name=user.last_name,
                first_intro="We received a request to reset the password for your Lightyear Electrical Goods Trading account.",
                second_intro="Click the button below to choose a new password.",
                invite_link=action_url,
                button="RESET PASSWORD",
                exp_notice="This link expires in 1 hour and can only be used once.",
                ending_title="Didn't request this?",
                ending_body="No action is needed — your password won't change. If you're concerned about your account security, please contact us at legt@gmail.com.",
                regards="Thanks,",
                team="The LEGT Team",
                footer="For your security, Lighyear Electrical Goods Trading will never ask for your password by email."
            )

            message = EmailMessage(
                to=user.email,
                subject="Password Reset",
                body=(
                    "We received a request to reset your password.\n\n"
                    "Please use the link below to set a new password."
                ),
                html=html
            )

            self.email_service.send(message)
            self.db.commit()

        except InvalidEmailAddressError:

            self.db.rollback()
            raise
            
        except Exception as error:

            self.db.rollback()
            raise EmailServiceFailedError() from error


    def set_user_new_password(
        self,
        token_hash: str,
        new_password: str 
    ) -> None:

        hash_token = hash_registration_token(token_hash)
        user = self.repository.get_user_by_token_hash(hash_token)
        now = datetime.now(timezone.utc).replace(tzinfo=None)

        if user is None:
            raise InvalidRegistrationTokenError()

        if user.email_verified is True:
            raise InvalidRegistrationTokenError()

        if user.token_expire is None or user.token_expire <= now:
            raise InvalidRegistrationTokenError()
    
        try:

            self.repository.set_hash_password(
                stored_user=user,
                new_hash_password=new_password
            )

            self.db.commit()

        except Exception as error:
        
            self.db.rollback()
            raise SetupNewPasswordError() from error


    def get_all_users(
        self,
        page: int,
        limit: int,
        search: str | None = None,
        role: UserRole | None = None,
        status: Literal["active", "disabled"] | None = None,
    ) -> UserPageListResponse:
    
        users, total = self.repository.get_all(
            page=page,
            limit=limit,
            search=search,
            role=role,
            status=status,
        )

        pages = ceil(total / limit) if total else 0

        return {
            "items": users,
            "page": page,
            "limit": limit,
            "total": total,
            "pages": pages,
        }


    def get_user_by_email(
        self, 
        email: str
    ) -> User:

        email = EmailValidation(email=email)
        user = self.repository.get_by_email(email.validated_email)

        if user is None:
            raise InvalidEmailAddressError()

        return user


    def get_user_by_id(
        self,
        user_id: int
    ) -> User:

        user = self.repository.get_by_id(user_id)

        if user is None:
            raise InvalidCredentialsError()

        return user


    def enable_user(
        self,
        user_id: int,
        actor_id: int 
    ) -> None:

        user = self.repository.get_by_id(user_id)

        if user is None:
            raise InvalidCredentialsError()

        now = datetime.now(timezone.utc).replace(tzinfo=None)

        try:
            
            self.repository.enable(
                stored_user=user,
                approve_by=actor_id,
                now=now
            )

            self.db.commit()
        
        except Exception as error:

            self.db.rollback()
            raise InvalidCredentialsError() from error


    def disable_user(
        self,
        user_id: int,
        actor_id: int 
    ) -> None:

        if actor_id == user_id:
            raise InsufficientPermissionsError(
                detail="You cannot disable your own account"
            )

        user = self.repository.get_by_id(user_id)

        if user is None:
            raise InvalidCredentialsError()

        now = datetime.now(timezone.utc).replace(tzinfo=None)

        try:
            
            self.repository.disable(
                stored_user=user,
                approve_by=actor_id,
                now=now
            )

            self.db.commit()
        
        except Exception as error:

            self.db.rollback()
            raise InvalidCredentialsError() from error


    def promote_user(
        self,
        user_id: int,
        actor_id: int
    ) -> None:

        user = self.repository.get_by_id(user_id)

        if user is None:
            raise InvalidCredentialsError()

        now = datetime.now(timezone.utc).replace(tzinfo=None)

        try:

            self.repository.promote(
                stored_user=user,
                approve_by=actor_id,
                now=now
            )

            self.db.commit()

        except Exception as error:

            self.db.rollback()
            raise InvalidCredentialsError() from error


    def demote_user(
        self,
        user_id: int,
        actor_id: int
    ) -> None:

        if actor_id == user_id:
            raise InsufficientPermissionsError(
                detail="You cannot demote your own account"
            )

        user = self.repository.get_by_id(user_id)

        if user is None:
            raise InvalidCredentialsError()

        now = datetime.now(timezone.utc).replace(tzinfo=None)

        try:

            self.repository.demote(
                stored_user=user,
                approve_by=actor_id,
                now=now
            )

            self.db.commit()

        except Exception as error:

            self.db.rollback()
            raise InvalidCredentialsError() from error


    def delete_user(
        self,
        user_id: int,
        actor_id: int
    ) -> None:

        if actor_id == user_id:
            raise InsufficientPermissionsError(
                detail="You cannot permanently delete your own account"
            )

        user = self.repository.get_by_id_for_soft_deletion(user_id)

        if user is None:
            raise InvalidCredentialsError()

        now = datetime.now(timezone.utc).replace(tzinfo=None)

        try:

            self.repository.delete(
                stored_user=user,
                approve_by=actor_id,
                now=now
            )

            self.db.commit()

        except Exception as error:

            self.db.rollback()

            print(error)
            raise InvalidCredentialsError() from error


    def get_active_user_counts(
        self
    ) -> int:

        return self.repository.count_active_users()
