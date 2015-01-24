from app.models.user import User
from django.test import TestCase
from emailusernames.utils import (
    create_user,
    get_user,
    user_exists)

class TestUser(TestCase):
    fixtures = ['23_auth_user']

    def test_user_create_success_given_all_info(self):
        create_user('test@testing.ave', 'password')
        user = User.objects.get(email='test@testing.ave')
        self.assertIsNotNone(user)
        self.assertEqual(user.email,'test@testing.ave')
        self.assertTrue(user.check_password('password'))

    def test_user_create_success_when_email_given(self):
        create_user(email='test@testing.ave')
        user = User.objects.get(email='test@testing.ave')
        self.assertIsNotNone(user)
    
    def test_user_create_failed_when_email_missing(self):
        with self.assertRaises(Exception):
            user_error = create_user(None, "bad_password")
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

