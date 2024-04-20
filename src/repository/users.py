from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas.schemas import UserIn, UserOut


async def get_user_by_email(email: str, db: Session) -> UserOut:
    """
    Retrieves a user by their email address.

    :param str email: The email address of the user to retrieve.
    :param Session db: The database session object.

    :return: The user corresponding to the provided email, or None if not found.
    :rtype: UserOut or None
    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserIn, db: Session) -> User:
    """
    Creates a new user.

    :param UserIn body: The data for the new user.
    :param Session db: The database session object.

    :return: The newly created user.
    :rtype: User
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    Updates the refresh token for a user.

    :param User user: The user whose token is to be updated.
    :param str | None token: The new refresh token. Pass None to remove the token.
    :param Session db: The database session object.

    :return: This function does not return anything.
    :rtype: None
    """
    user.refresh_token = token
    db.commit()


async def confirm_email(email: str, db: Session) -> None:
    """
    Marks a user's email as confirmed.

    :param str email: The email address of the user to confirm.
    :param Session db: The database session object.

    :return: This function does not return anything.
    :rtype: None
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email, url: str, db: Session) -> UserOut:
    """
    Updates the avatar URL for a user.

    :param str email: The email address of the user to update.
    :param str url: The new URL of the avatar.
    :param Session db: The database session object.

    :return: The updated user with the new avatar URL.
    :rtype: UserOut
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
