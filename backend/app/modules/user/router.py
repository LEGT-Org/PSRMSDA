from typing import Annotated 

from fastapi import (
    APIRouter, 
    Depends, 
    HTTPException, 
    Response,
    Cookie,
    status
)

from app.modules.user.schema import UserCreate, UserResponse, UserRole
from app.modules.user.service import UserService
from app.modules.user.model import User

from app.shared.dependencies.user import get_user_service
from app.shared.dependencies.auth import require_role
from app.shared.security.csrf import validate_csrf


router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.post(
    "/admin/register", 
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    data: UserCreate,
    service: Annotated[
        UserService,
        Depends(get_user_service)
    ],
    current_user: Annotated[
        User,
        Depends(require_role(UserRole.ADMIN))
    ],
    _: Annotated[None, Depends(validate_csrf)] = None
):

    try:

        return service.create_user(data)

    except EmailAlreadyExistsError:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists."
        )

    except InvalidEmailAddressError:

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Invalid email address."
        )

    except InvalidNameError:

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Name cannot be empty."
        )

    except NameMustBeTwoToFiftyCharacterError:

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Name must be between 2 and 50 characters."
        )

    except NameOnlyContainAlphabeticCharacterError:

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Name can only contain alphabetic characters, spaces, hypens, and apostrophes."
        )

