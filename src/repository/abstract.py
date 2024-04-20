import abc

from src.schemas.schemas import UserOut, ContactOut, ContactIn


class AbstractContactsRepository(abc.ABC):
    """
    Abstract base class defining the interface for a contacts repository.

    This class defines the abstract methods that should be implemented by concrete subclasses to provide
    functionality for managing contacts.

    """
    @abc.abstractmethod
    async def get_contacts(self, skip: int, limit: int, user: UserOut) -> list[ContactOut]:
        ...

    @abc.abstractmethod
    async def get_contact(self, contact_id: int, user: UserOut) -> ContactOut:
        ...

    @abc.abstractmethod
    async def create_contact(self, body: ContactIn, user: UserOut) -> ContactOut:
        ...

    @abc.abstractmethod
    async def remove_contact(self, contact_id: int, user: UserOut) -> ContactOut | None:
        ...

    @abc.abstractmethod
    async def update_contact(self, contact_id: int, body: ContactIn, user: UserOut) -> ContactOut | None:
        ...

    @abc.abstractmethod
    async def get_contacts_by_query(self, query: str, skip: int, limit: int, user: UserOut) -> list[ContactOut]:
        ...

    @abc.abstractmethod
    async def get_contacts_with_upcoming_birthdays(self, user: UserOut) -> list[ContactOut]:
        ...