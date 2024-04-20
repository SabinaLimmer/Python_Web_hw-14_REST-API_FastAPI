from fastapi import Depends

from src.database.db import get_db
from src.repository.contacts import ContactsRepository


def get_contacts_repository(db=Depends(get_db)):
    """
    Dependency function to get an instance of the ContactsRepository.

    :param db: Dependency on the database session.
    :type db: Depends
    :return: An instance of ContactsRepository.
    :rtype: ContactsRepository
    """
    return ContactsRepository(db)