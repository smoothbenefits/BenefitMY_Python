from app.models.user import User
from django.test import TestCase
from emailusernames.utils import (
    create_user,
    get_user,
    user_exists)

class TestUser(TestCase):

    def test_user_create(self):
        user_email = "user1234@live.com"
        user_password = "kaceycute"
        user_new = create_user(user_email, user_password)
        self.assertTrue(user_exists(user_email))
        retrieved_user = get_user(user_email)
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.email, user_email)
        self.assertTrue(retrieved_user.check_password(user_password))

    fixtures = ['user']

    def test_user_basic(self):
        user1=User.objects.get(pk=11)
        self.assertTrue(user1)
        self.assertIsNotNone(user1.email)
        self.assertEqual(user1.email, "user1@benefitmy.com")
        username = user1.get_username()
        self.assertEqual(username, "user1")

    def test_user_password(self):
        user2 = User.objects.get(pk=12)
        self.assertTrue(user2)
        self.assertIsNotNone(user2.email)
        self.assertEqual(user2.email, "user2@benefitmy.com")
        user2.set_password("the_password")
        self.assertTrue(user2.check_password("the_password"))

    def test_non_exist_user(self):
        with self.assertRaises(User.DoesNotExist):
            user_non_exist = User.objects.get(pk=55)

