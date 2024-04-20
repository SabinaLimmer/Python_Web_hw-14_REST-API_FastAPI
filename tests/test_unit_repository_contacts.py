from datetime import date
import unittest
from unittest.mock import MagicMock

from sqlalchemy import extract
from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas.schemas import ContactIn
from src.repository.contacts import ContactsRepository

class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.contacts_repository = ContactsRepository(db=self.session)
        self.user = User(id=1)

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await self.contacts_repository.get_contacts(skip=0, limit=10, user=self.user)
        self.assertEqual(result, contacts)

    async def test_get_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await self.contacts_repository.get_contact(contact_id=1, user=self.user)
        self.assertEqual(result, contact)

    async def test_get_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await self.contacts_repository.get_contact(contact_id=1, user=self.user)
        self.assertIsNone(result)

    async def test_create_contact(self):
        body = ContactIn(
            first_name="Test", 
            last_name="test", 
            email="test@test.com", 
            phone_number="+48505606404", 
            date_of_birth = date(1998, 2, 28), 
            done=False
            )
        result = await self.contacts_repository.create_contact(body=body, user=self.user)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone_number, body.phone_number)
        self.assertEqual(result.date_of_birth, body.date_of_birth)
        self.assertTrue(hasattr(result, "id"))

    async def test_remove_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await self.contacts_repository.remove_contact(contact_id=1, user=self.user)
        self.assertEqual(result, contact)

    async def test_remove_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await self.contacts_repository.remove_contact(contact_id=1, user=self.user)
        self.assertIsNone(result)

    async def test_update_contact_found(self):
        body = ContactIn(
            first_name="Test", 
            last_name="test", 
            email="test@test.com", 
            phone_number="+48505606404", 
            date_of_birth = date(1998, 2, 28), 
            done=True
            )
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        self.session.commit.return_value = None
        result = await self.contacts_repository.update_contact(contact_id=1, body=body, user=self.user)
        self.assertEqual(result, contact)

    async def test_update_contact_not_found(self):
        body = ContactIn(
            first_name="Test", 
            last_name="test", 
            email="test@test.com", 
            phone_number="+48505606404", 
            date_of_birth = date(1998, 2, 28), 
            done=True
            )
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await self.contacts_repository.update_contact(contact_id=1, body=body, user=self.user)
        self.assertIsNone(result)

    async def test_get_contacts_by_query(self):
        query = "Test"
        skip = 0
        limit = 10
        contacts = [
            Contact(
                first_name="Test", 
                last_name="test", 
                email="test@test.com", 
                phone_number="+48505606404", 
                date_of_birth = date(1998, 2, 28), 
                ),
            Contact(
                first_name="Test2", 
                last_name="test2", 
                email="test2@test.com", 
                phone_number="+48505606403", 
                date_of_birth = date(1998, 1, 22), 
                ),
        ]
        self.session.query().filter().filter().offset().limit().all.return_value = contacts
        result = await self.contacts_repository.get_contacts_by_query(query, skip, limit, self.user)
        self.assertEqual(result, contacts)
        self.session.query().filter().filter().offset().limit().all.assert_called_once()

    async def test_get_contacts_with_upcoming_birthdays(self):
        contacts = [Contact(), Contact()]
        self.session.query().filter().filter().all.return_value = contacts
        result = await self.contacts_repository.get_contacts_with_upcoming_birthdays(self.user)
        self.assertEqual(result, contacts)
        self.session.query().filter().filter().all.assert_called_once()


if __name__ == '__main__':
    unittest.main()
