import pickle
from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader

from src.database.db import get_db
from src.database.models import User
from src.repository import users as repository_users
from src.services.auth import Auth, auth_service
from src.conf.config import settings
from src.schemas.schemas import UserOut

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserOut)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    """
    Retrieve details of the current user.

    :param User current_user: The current authenticated user.

    :return: Details of the current user.
    :rtype: UserOut
    """
    return current_user

@router.patch('/avatar', response_model=UserOut)
async def update_avatar_user(file: UploadFile = File(), current_user: User = Depends(auth_service.get_current_user),
                             db: Session = Depends(get_db)):
    """
    Update the avatar of the current user.

    :param UploadFile file: The image file to upload as the avatar.
    :param User current_user: The current authenticated user.
    :param Session db: The database session.

    :return: Updated user details with the new avatar.
    :rtype: UserOut

    :raises HTTPException: If there is an issue updating the avatar.
    """
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )

    r = cloudinary.uploader.upload(file.file, public_id=f'ContactsApp/{current_user.username}', overwrite=True)
    src_url = cloudinary.CloudinaryImage(f'ContactsApp/{current_user.username}')\
                        .build_url(width=250, height=250, crop='fill', version=r.get('version'))
    user = await repository_users.update_avatar(current_user.email, src_url, db)
    Auth.r.set(f"user:{user.email}", pickle.dumps(user))
    return user
