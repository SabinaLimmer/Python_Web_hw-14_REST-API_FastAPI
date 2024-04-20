from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from sqlalchemy import extract, or_

from src.database.models import Contact
from src.schemas.schemas import ContactIn, UserOut, ContactOut
from src.repository.abstract import AbstractContactsRepository

class ContactsRepository(AbstractContactsRepository):
    """
    Repository for contacts.
    """
    def __init__(self, db: Session):
        self._db = db

    async def get_contacts(self, skip: int, limit: int, user: UserOut) -> list[ContactOut]:
        """
        Retrieves a list of contacts for a specific user with specified pagination parameters.

        :param skip: The number of contacts to skip.
        :type skip: int
        :param limit: The maximum number of contacts to return.
        :type limit: int
        :param user: The user to retrieve contacts for.
        :type user: UserOut
        :return: A list of contacts.
        :rtype: List[ContactOut]
        """
        return self._db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


    async def get_contact(self, contact_id: int, user: UserOut) -> ContactOut:
        """
        Retrieves a single contact with the specified ID for a specific user.

        :param contact_id: The ID of the contact to retrieve.
        :type contact_id: int
        :param user: The user to retrieve the contact for.
        :type user: UserOut
        :return: The contact with the specified ID, or None if it does not exist.
        :rtype: ContactOut | None
        """
        return self._db.query(Contact).filter(Contact.id == contact_id, Contact.user_id == user.id).first()


    async def create_contact(self, body: ContactIn, user: UserOut) -> ContactOut:
        """
        Creates a new contact for a specific user.

        :param body: The data for the contact to create.
        :type body: ContactIn
        :param user: The user to create the contact for.
        :type user: UserOut
        :return: The newly created contact.
        :rtype: ContactOut
        """
        contact = Contact(first_name=body.first_name, last_name=body.last_name, email=body.email, phone_number = body.phone_number, date_of_birth = body.date_of_birth, user_id=user.id)
        self._db.add(contact)
        self._db.commit()
        self._db.refresh(contact)
        return contact


    async def remove_contact(self, contact_id: int, user: UserOut) -> ContactOut | None:
        """
        Removes a single contact with the specified ID for a specific user.

        :param contact_id: The ID of the contact to remove.
        :type contact_id: int
        :param user: The user to remove the contact for.
        :type user: UserOut
        :return: The removed contact, or None if it does not exist.
        :rtype: ContactOut | None
        """
        contact = self._db.query(Contact).filter(Contact.id == contact_id, Contact.user_id == user.id).first()
        if contact:
            self._db.delete(contact)
            self._db.commit()
        return contact


    async def update_contact(self, contact_id: int, body: ContactIn, user: UserOut) -> ContactOut | None:
        """
        Updates a single contact with the specified ID for a specific user.

        :param contact_id: The ID of the contact to update.
        :type contact_id: int
        :param body: The updated data for the contact.
        :type body: ContactIn
        :param user: The user to update the contact for.
        :type user: UserOut
        :return: The updated contact, or None if it does not exist.
        :rtype: ContactOut | None
        """
        contact = self._db.query(Contact).filter(Contact.id == contact_id, Contact.user_id == user.id).first()
        if contact:
            contact.first_name = body.first_name
            contact.last_name = body.last_name
            contact.email = body.email
            contact.phone_number = body.phone_number
            contact.date_of_birth = body.date_of_birth
            self._db.commit()
        return contact


    async def get_contacts_by_query(self, query: str, skip: int, limit: int, user: UserOut) -> list[ContactOut]:
        """
        Retrieves a list of contacts based on a search query for a specific user.

        :param query: The search query to filter contacts by (can be a partial match for first name, last name, or email).
        :type query: str
        :param skip: The number of contacts to skip.
        :type skip: int
        :param limit: The maximum number of contacts to return.
        :type limit: int
        :param user: The user whose contacts are being queried.
        :type user: UserOut
        :return: A list of contacts matching the search query within the specified range.
        :rtype: list[ContactOut]
        """
        contact = self._db.query(Contact).filter(Contact.user_id == user.id)
        if query:
            return contact.filter(
                or_(
                    Contact.first_name.ilike(f"%{query}%"),
                    Contact.last_name.ilike(f"%{query}%"),
                    Contact.email.ilike(f"%{query}%")
                )
            ).offset(skip).limit(limit).all()


    async def get_contacts_with_upcoming_birthdays(self, user: UserOut) -> list[ContactOut]:
        """
        Retrieves a list of contacts with upcoming birthdays within the next 7 days for a specific user.

        :param user: The user whose contacts are being queried.
        :type user: UserOut
        :return: A list of contacts with birthdays in the next 7 days.
        :rtype: list[ContactOut]
        """
        contact = self._db.query(Contact).filter(Contact.user_id == user.id)
        today = datetime.today()
        end_date = today + timedelta(days=7)
        return contact.filter(
            extract('month', Contact.date_of_birth) == today.month,
            extract('day', Contact.date_of_birth) >= today.day,
            extract('day', Contact.date_of_birth) <= end_date.day
        ).all()
