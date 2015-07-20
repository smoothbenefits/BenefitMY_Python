import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from view_test_base import ViewTestBase

User = get_user_model()

class LoginViewTestCase(TestCase, ViewTestBase):
    fixtures = ['24_person', '23_auth_user', '10_company']

    def setUp(self):
        self.user_password = 'foobar'
        self.broker_user = User.objects.get(email='user1@benefitmy.com')
        self.broker_user.set_password(self.user_password)
        self.broker_user.save()

    def test_get_not_logged_in(self):
        response = self.client.get(reverse('current_user'))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)

    def test_login_exist_user(self):
        login_response = self.client.post(reverse('user_login'), {'email':self.broker_user.get_username(), 'password':self.user_password})
        self.assertIsNotNone(login_response)
        self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual(self.client.session['_auth_user_id'], self.broker_user.id)
        self.assertEqual(login_response.status_code, 302)
        self.assertIn('/dashboard/', login_response.url)

    def test_login_nonexist_user(self):
        login_response = self.client.post(reverse('user_login'), {'email':'nonexist@bad.com', 'password':self.user_password})
        self.assertIsNotNone(login_response)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_logout_succeed(self):
        login_response = self.client.post(reverse('user_login'), {'email':self.broker_user.get_username(), 'password':self.user_password})
        self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual(self.client.session['_auth_user_id'], self.broker_user.id)
        self.assertEqual(login_response.status_code, 302)
        self.assertIn('/dashboard/', login_response.url)
        logout_response = self.client.delete(reverse('user_logout'))
        self.assertTrue(logout_response.status_code, 200)
        self.assertEqual(logout_response.content, 'done')
        # Make sure the user is now logged out
        response = self.client.get(reverse('current_user'))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)

    def test_logout_bad_method(self):
        login_response = self.client.post(reverse('user_login'), {'email':self.broker_user.get_username(), 'password':self.user_password})
        self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual(self.client.session['_auth_user_id'], self.broker_user.id)
        self.assertEqual(login_response.status_code, 302)
        self.assertIn('/dashboard/', login_response.url)
        logout_response = self.client.post(reverse('user_logout'))
        self.assertTrue(logout_response.status_code, 200)
        self.assertEqual(logout_response.content, '')
        # Make sure the user is not logged out
        response = self.client.get(reverse('current_user'))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.content, '')
