from django.test import TestCase
from django.contrib.auth import get_user_model

from app.custom_authentication import AuthUserManager

User = get_user_model()

class TestUser(TestCase):
    fixtures = ['23_auth_user']

    def test_user_create_success_given_all_info(self):
        User.objects.create_user(email='test@testing.ave', password='password')
        user = User.objects.get(email='test@testing.ave')
        self.assertIsNotNone(user)
        self.assertEqual(user.email,'test@testing.ave')
        self.assertTrue(user.check_password('password'))

    def test_user_create_success_when_email_given(self):
        User.objects.create_user(email='test@testing.ave')
        user = User.objects.get(email='test@testing.ave')
        self.assertIsNotNone(user)

    def test_user_create_failed_when_email_missing(self):
        with self.assertRaises(ValueError):
            user_error = User.objects.create_user(None, "bad_password")
            self.assertIsNone(user_error)

    def test_get_user_by_id_success_when_user_exists(self):
        user1=User.objects.get(pk=1)
        self.assertTrue(user1)
        self.assertIsNotNone(user1.email)
        self.assertEqual(user1.email, "user1@benefitmy.com")
        username = user1.get_username()
        self.assertEqual(username, "user1@benefitmy.com")

    def test_user_password(self):
        user2 = User.objects.get(pk=2)
        self.assertTrue(user2)
        self.assertIsNotNone(user2.email)
        self.assertEqual(user2.email, "user2@benefitmy.com")
        user2.set_password("the_password")
        self.assertTrue(user2.check_password("the_password"))

    def test_non_exist_user(self):
        with self.assertRaises(User.DoesNotExist):
            user_non_exist = User.objects.get(pk=55)

    def test_manager_user_exists_returns_true_when_user_exists(self):
        manager = AuthUserManager()
        exists = manager.user_exists(email='user1@benefitmy.com')
        self.assertTrue(exists)

    def test_manager_user_exists_returns_false_when_user_not_exists(self):
        manager = AuthUserManager()
        exists = manager.user_exists(email='this_user@not.exists')
        self.assertFalse(exists)

    def test_manager_get_user_return_correct_value(self):
        manager = AuthUserManager()
        expectedEmail = 'user1@benefitmy.com'
        user = manager.get_user(expectedEmail)
        self.assertEqual(expectedEmail, user.email)

    def test_manager_get_user_return_none_when_user_not_exists(self):
        manager = AuthUserManager()
        email = 'this_user@not.exists'
        user = manager.get_user(email)
        self.assertEqual(None, user)
