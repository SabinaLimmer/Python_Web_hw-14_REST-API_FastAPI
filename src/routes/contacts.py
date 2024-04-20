from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi_limiter.depends import RateLimiter

from src.schemas.schemas import ContactIn, ContactOut, UserOut
from src.repository.abstract import AbstractContactsRepository
from src.services.auth import auth_service

from src.dependencies import get_contacts_repository


router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/", response_model=List[ContactOut], description="No more than 10 requests per minute", dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_contacts(skip: int = 0, limit: int = 100,
                        repository_contacts: AbstractContactsRepository = Depends(get_contacts_repository),
                        current_user: UserOut = Depends(auth_service.get_current_user)):
    """
    Retrieve a list of contacts for the current user with pagination.

    :param int skip: Number of contacts to skip. Defaults to 0.
    :param int limit: Maximum number of contacts to return. Defaults to 100.
    :param AbstractContactsRepository repository_contacts: The contacts repository.
    :param UserOut current_user: The current user.

    :return: A list of contacts.
    :rtype: List[ContactOut]

    :raises HTTPException: If there is an issue retrieving the contacts.
    """
    contacts = await repository_contacts.get_contacts(skip, limit, current_user)
    return contacts


@router.get("/{contact_id}", response_model=ContactOut)
async def read_contact(contact_id: int,
                        repository_contacts: AbstractContactsRepository = Depends(get_contacts_repository),
                        current_user: UserOut = Depends(auth_service.get_current_user)):
    """
    Retrieve a single contact by ID.

    :param int contact_id: The ID of the contact to retrieve.
    :param AbstractContactsRepository repository_contacts: The contacts repository.
    :param UserOut current_user: The current user.

    :return: The contact information.
    :rtype: ContactOut

    :raises HTTPException: If the contact with the specified ID does not exist.
    """
    contact = await repository_contacts.get_contact(contact_id, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="contact not found")
    return contact


@router.post("/", response_model=ContactOut)
async def create_contact(body: ContactIn,
                        repository_contacts: AbstractContactsRepository = Depends(get_contacts_repository),
                        current_user: UserOut = Depends(auth_service.get_current_user)):
    """
    Create a new contact.

    :param ContactIn body: The contact data.
    :param AbstractContactsRepository repository_contacts: The contacts repository.
    :param UserOut current_user: The current user.

    :return: The newly created contact.
    :rtype: ContactOut

    :raises HTTPException: If there is an issue creating the contact.
    """
    return await repository_contacts.create_contact(body, current_user)


@router.put("/{contact_id}", response_model=ContactOut)
async def update_contact(body: ContactIn, contact_id: int,
                        repository_contacts: AbstractContactsRepository = Depends(get_contacts_repository),
                        current_user: UserOut = Depends(auth_service.get_current_user)):
    """
    Update an existing contact.

    :param ContactIn body: The updated contact data.
    :param int contact_id: The ID of the contact to update.
    :param AbstractContactsRepository repository_contacts: The contacts repository.
    :param UserOut current_user: The current user.

    :return: The updated contact information.
    :rtype: ContactOut

    :raises HTTPException: If the contact with the specified ID does not exist.
    """
    contact = await repository_contacts.update_contact(contact_id, body, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="contact not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactOut)
async def remove_contact(contact_id: int,
                        repository_contacts: AbstractContactsRepository = Depends(get_contacts_repository),
                        current_user: UserOut = Depends(auth_service.get_current_user)):
    """
    Remove a contact.

    :param int contact_id: The ID of the contact to remove.
    :param AbstractContactsRepository repository_contacts: The contacts repository.
    :param UserOut current_user: The current user.

    :return: The removed contact.
    :rtype: ContactOut

    :raises HTTPException: If the contact with the specified ID does not exist.
    """
    contact = await repository_contacts.remove_contact(contact_id, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="contact not found")
    return contact


@router.get("/search/", response_model=List[ContactOut])
async def search_contacts(query: str, skip: int = 0, limit: int = 100,
                        repository_contacts: AbstractContactsRepository = Depends(get_contacts_repository),
                        current_user: UserOut = Depends(auth_service.get_current_user)):
    """
    Search contacts by query.

    :param str query: The search query.
    :param int skip: Number of contacts to skip. Defaults to 0.
    :param int limit: Maximum number of contacts to return. Defaults to 100.
    :param AbstractContactsRepository repository_contacts: The contacts repository.
    :param UserOut current_user: The current user.

    :return: A list of contacts matching the query.
    :rtype: List[ContactOut]
    """
    contacts = await repository_contacts.get_contacts_by_query(query, skip, limit, current_user)
    return contacts


@router.get("/upcoming-birthdays/", response_model=List[ContactOut])
async def get_contacts_upcoming_birthdays(
                        repository_contacts: AbstractContactsRepository = Depends(get_contacts_repository),
                        current_user: UserOut = Depends(auth_service.get_current_user)):
    """
    Retrieve contacts with upcoming birthdays.

    :param AbstractContactsRepository repository_contacts: The contacts repository.
    :param UserOut current_user: The current user.

    :return: A list of contacts with upcoming birthdays.
    :rtype: List[ContactOut]
    """
    contacts = await repository_contacts.get_contacts_with_upcoming_birthdays(current_user)
    return contacts