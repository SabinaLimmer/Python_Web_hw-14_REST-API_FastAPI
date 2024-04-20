from datetime import date
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class ContactIn(BaseModel):
    """
    Schema for incoming contact data during creation.
    """
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: str
    phone_number: str = Field(max_length=15)
    date_of_birth: date


class ContactOut(ContactIn):
    """
    Schema for outgoing contact data.
    """
    id: int


    class Config:
        orm_mode = True


class UserIn(BaseModel):
    """
    Schema for incoming user data during creation.
    """
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserOut(BaseModel):
    """
    Schema for outgoing user data.
    """
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True


class UserCreated(BaseModel):
    """
    Schema for response after creating a new user.
    """
    user: UserOut
    detail: str = "User successfully created"


class Token(BaseModel):
    """
    Schema for authentication token.
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RequestEmail(BaseModel):
    """
    Schema for request email data.
    """
    email: EmailStr
