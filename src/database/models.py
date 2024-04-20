from sqlalchemy import Column, Integer, String, Date, Boolean, func
from sqlalchemy.sql.sqltypes import Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.orm import relationship

Base = declarative_base()

class Contact(Base):
    """
    Model representing a contact.

    Attributes:
        id (int): The primary key ID of the contact.
        first_name (str): The first name of the contact.
        last_name (str): The last name of the contact.
        email (str): The email address of the contact (must be unique).
        phone_number (str): The phone number of the contact.
        date_of_birth (Date): The date of birth of the contact.
        user_id (int): The ID of the user to whom the contact belongs.
        user (relationship): Relationship with the User model.

    """
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, index=True)
    date_of_birth = Column(Date)
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    user = relationship('User', backref="contacts")

class User(Base):
    """
    Model representing a user.

    Attributes:
        id (int): The primary key ID of the user.
        username (str): The username of the user.
        email (str): The email address of the user (must be unique).
        confirmed (bool): Flag indicating whether the user's email has been confirmed.
        password (str): The hashed password of the user.
        created_at (DateTime): The timestamp indicating when the user account was created.
        avatar (str): The URL of the user's avatar.
        refresh_token (str): The refresh token used for authentication.

    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    confirmed = Column(Boolean, default=False)
    password = Column(String(255), nullable=False)
    created_at = Column('crated_at', DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
