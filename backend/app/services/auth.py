from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.repositories.user import create_user, get_user_by_email
from app.schemas.auth import UserLogin, UserRegister


class EmailAlreadyExistsError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


def register_user(db: Session, user_data: UserRegister) -> User:
    existing_user = get_user_by_email(db, user_data.email)

    if existing_user is not None:
        raise EmailAlreadyExistsError

    hashed_password = hash_password(user_data.password)

    return create_user(
        db=db,
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
    )


def authenticate_user(db: Session, user_data: UserLogin) -> User:
    user = get_user_by_email(db, user_data.email)

    if user is None:
        raise InvalidCredentialsError

    if not verify_password(user_data.password, user.hashed_password):
        raise InvalidCredentialsError

    if not user.is_active:
        raise InvalidCredentialsError

    return user