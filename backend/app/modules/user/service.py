from datetime import datetime, timedelta, timezone
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.modules.user.repository import UserRepository
from app.modules.user.schema import UserRole, UserCreate
from app.modules.user.model import User

from app.shared.email import EmailService, EmailMessage, JinjaEmailRendered
from app.shared.value_object.user import User
from app.shared.config import settings
from app.shared.security.password import (
    generate_registration_token,
    hash_registration_token, 
    hash_password
)

from app.shared.exception import (
    EmailAlreadyExistsError, 
    InvalidCredentialsError,
    EmailServiceFailedError
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
        data: UserCreate
    ) -> User:

        user = User(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email
        )

        if self.repository.get_by_email(user.validated_email):
            raise EmailAlreadyExistsError()

        now = datetime.now(timezone.utc)

        raw_token = generate_registration_token()
        token_hash = hash_registration_token(raw_token)
        token_expire = now + timedelta(hours=settings.auth.password_setup_token_expire_hours)
        
        user = User(
            first_name=user.validated_first_name,
            last_name=user.validated_last_name,
            email=user.validated_email,
            password_hash=None,
            role=UserRole.USER,
            token_hash=token_hash,
            token_expire=token_expire,
            email_verified=False,
            is_active=True,
            created_at=now,
            updated_at=now,
            deleted_at=None
        )

        self.repository.create(user)

        try:

            action_url = (
                f"{settings.frontend.url}/set-password"
                f"?token={raw_token}"
            )

            html = self.email_renderer.render(
                "set_your_password.html",

                title="Set Your Password",
                logo_url="/app/shared/email/template/LEGT-Logo.png",
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

        except EmailServiceFailedError:

            self.db.rollback()
            raise EmailServiceFailedError()


    def get_user_by_email(
        self, 
        email: EmailStr
    ) -> User:

        email = Email(email)
        user = self.repository.get_by_email(email.validated_email)

        if user is None:
            raise InvalidCredentialsError()

        return user


    def get_user_by_id(
        self,
        user_id: int
    ) -> User:

        user = self.repository.get_by_id(user_id)

        return user