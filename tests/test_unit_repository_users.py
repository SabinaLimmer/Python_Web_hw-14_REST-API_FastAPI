import unittest
from unittest.mock import MagicMock, patch
from src.repository.users import (
    get_user_by_email, create_user, update_token, confirm_email, update_avatar
)
from src.database.models import User
from src.schemas.schemas import UserIn
from sqlalchemy.orm import Session


class TestUsersRepository(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)

    async def test_get_user_by_email(self):
        email = "test@test.com"
        user = User(email=email)
        self.session.query().filter().first.return_value = user
        result = await get_user_by_email(email, self.session)
        self.assertEqual(result, user)

    @patch("libgravatar.Gravatar.get_image", side_effect=Exception)
    async def test_create_user(self, mock_gravatar):
        user = UserIn(
            username="Test1",
            email="test@test.com",
            password="Test123",
        )
        with self.assertRaises(Exception):
            await create_user(user)
           
    async def test_update_token(self):
        user = User(email="test@test.com")
        token = "test"
        await update_token(user, token, self.session)
        self.assertEqual(user.refresh_token, token)
        self.session.commit.assert_called_once()

    async def test_confirm_email(self):
        email = "test@test.com"
        user = User(email=email)
        self.session.query().filter().first.return_value = user
        await confirm_email(email, self.session)
        self.assertTrue(user.confirmed)
        self.session.commit.assert_called_once()

    async def test_update_avatar(self):
        email = "test@test.com"
        url = "https://test.com/avatar.jpg"
        user = User(email=email)
        self.session.query().filter().first.return_value = user
        result = await update_avatar(email, url, self.session)
        self.assertEqual(result.avatar, url)
        self.session.commit.assert_called_once()


if __name__ == '__main__':
    unittest.main()
