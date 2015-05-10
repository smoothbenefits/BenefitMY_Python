import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from view_test_base import ViewTestBase

User = get_user_model()

class UserViewTestCase(TestCase, ViewTestBase):

    fixtures = ['24_person', 
                '10_company', 
                '23_auth_user', 
                '11_address',
                '12_phone', 
                '34_company_user']

    def setUp(self):
        self.user_password = 'foobar'
        self.broker_user = User.objects.get(email='user1@benefitmy.com')
        self.broker_user.set_password(self.user_password)
        self.broker_user.save()
        self.admin_user = User.objects.get(email='user2@benefitmy.com')
        self.admin_user.set_password(self.user_password)
        self.admin_user.save()
        self.employee_user = User.objects.get(email='user3@benefitmy.com')
        self.employee_user.set_password(self.user_password)
        self.employee_user.save()

    def test_get_cur_user_broker(self):
        login_response = self.client.post(reverse('user_login'), {'email':self.broker_user.get_username(), 'password':self.user_password})
        response = self.client.get(reverse('current_user'))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.content, '')
        user_data = json.loads(response.content)
        self.assertTrue('user' in user_data)
        cur_user = user_data['user']
        self.assertTrue('id' in cur_user and cur_user['id'] == self.normalize_key(1))
        self.assertTrue('first_name' in cur_user and cur_user['first_name'] == 'John')
        self.assertTrue('last_name' in cur_user and cur_user['last_name'] == 'Hancock')
        self.assertTrue('email' in cur_user and cur_user['email'] == 'user1@benefitmy.com')
        self.assertIn('roles', user_data)
        roles = user_data['roles']
        for user_role in roles:
            self.assertTrue('company_user_type' in user_role and user_role['company_user_type'] == 'broker')

    def test_get_cur_user_employer(self):
        login_response = self.client.post(reverse('user_login'), {'email':self.admin_user.get_username(), 'password':self.user_password})
        response = self.client.get(reverse('current_user'))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.content, '')
        user_data = json.loads(response.content)
        self.assertTrue('user' in user_data)
        cur_user = user_data['user']
        self.assertTrue('id' in cur_user and cur_user['id'] == self.normalize_key(2))
        self.assertTrue('first_name' in cur_user and cur_user['first_name'] == 'Francis')
        self.assertTrue('last_name' in cur_user and cur_user['last_name'] == 'McLaurren')
        self.assertTrue('email' in cur_user and cur_user['email'] == 'user2@benefitmy.com')
        self.assertIn('roles', user_data)
        roles = user_data['roles']
        for user_role in roles:
            self.assertTrue('company_user_type' in user_role and user_role['company_user_type'] == 'admin')

    def test_get_cur_user_employee(self):
        login_response = self.client.post(reverse('user_login'), {'email':self.employee_user.get_username(), 'password':self.user_password})
        response = self.client.get(reverse('current_user'))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.content, '')
        user_data = json.loads(response.content)
        self.assertTrue('user' in user_data)
        cur_user = user_data['user']
        self.assertTrue('id' in cur_user and cur_user['id'] == self.normalize_key(3))
        self.assertTrue('first_name' in cur_user and cur_user['first_name'] == 'Simon')
        self.assertTrue('last_name' in cur_user and cur_user['last_name'] == 'Cowell')
        self.assertTrue('email' in cur_user and cur_user['email'] == 'user3@benefitmy.com')
        self.assertIn('roles', user_data)
        roles = user_data['roles']
        for user_role in roles:
            self.assertTrue('company_user_type' in user_role and user_role['company_user_type'] == 'employee')

    def test_get_user_by_id_cur_user(self):
        login_response = self.client.post(reverse('user_login'), {'email':self.employee_user.get_username(), 'password':self.user_password})
        response=self.client.get(reverse('user_by_id', kwargs={'pk':self.normalize_key(3)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.content, '')
        user_data = json.loads(response.content)
        self.assertTrue('user' in user_data)
        cur_user = user_data['user']
        self.assertTrue('id' in cur_user and cur_user['id'] == self.normalize_key(3))
        self.assertTrue('first_name' in cur_user and cur_user['first_name'] == 'Simon')
        self.assertTrue('last_name' in cur_user and cur_user['last_name'] == 'Cowell')
        self.assertTrue('email' in cur_user and cur_user['email'] == 'user3@benefitmy.com')

    def test_get_user_by_id_existing_user(self):
        login_response = self.client.post(reverse('user_login'), {'email':self.employee_user.get_username(), 'password':self.user_password})
        response=self.client.get(reverse('user_by_id', kwargs={'pk':self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.content, '')
        user_data = json.loads(response.content)
        self.assertTrue('user' in user_data)
        cur_user = user_data['user']
        self.assertTrue('id' in cur_user and cur_user['id'] == self.normalize_key(1))
        self.assertTrue('first_name' in cur_user and cur_user['first_name'] == 'John')
        self.assertTrue('last_name' in cur_user and cur_user['last_name'] == 'Hancock')
        self.assertTrue('email' in cur_user and cur_user['email'] == 'user1@benefitmy.com')

    def test_get_user_by_id_nonexisting(self):
        login_response = self.client.post(reverse('user_login'), {'email':self.broker_user.get_username(), 'password':self.user_password})
        response=self.client.get(reverse('user_by_id', kwargs={'pk':self.normalize_key(5000)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)

    def test_get_user_by_id_not_logged(self):
        response=self.client.get(reverse('user_by_id', kwargs={'pk':self.normalize_key(1)}))
        self.assertIsNotNone(response)
        # With proper authentication, the status code check below should be 401
        self.assertEqual(response.status_code, 200)

    # what is this test about?
    def test_get_all_users(self):
        login_response = self.client.post(reverse('user_login'), {'email':self.employee_user.get_username(), 'password':self.user_password})
        response=self.client.get(reverse('all_users'))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.content, '')
        all_user_data = json.loads(response.content)
        self.assertTrue('users' in all_user_data)
        all_users = all_user_data['users']
        self.assertEqual(len(all_users), 6)
        for user in all_users:
            self.assertIn('id', user)
            self.assertIn('first_name', user)
            self.assertIn('last_name', user)
            self.assertIn('email', user)

    def test_get_all_users_not_logged(self):
        response=self.client.get(reverse('all_users'))
        self.assertIsNotNone(response)
        # With proper authentication, the status code check below should be 401
        self.assertEqual(response.status_code, 200)


    def test_user_create_new_success(self):
        login_response = self.client.post(reverse('user_login'), {'email':self.admin_user.get_username(), 'password':self.user_password})
        new_user = {
            'user': {
                'first_name':'fiddfrstvvv5', 
                'last_name':'lastvvfdvv5', 
                'email':'user456@smoothbenefits.com'
                },
            'company': 1,
            'company_user_type': 'employee',
            'send_email': 'true',
            'create_docs': 'true',
            'fields':[
                {'company_name':'benefitmy'}, 
                {'position': 'Software Engineer'}]
        }
        response = self.client.post(reverse('all_users'), json.dumps(new_user), content_type='application/json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)
        created_user = json.loads(response.content)
        self.assertTrue('id' in created_user and created_user['id'])
        self.assertTrue('first_name' in created_user and created_user['first_name'] == new_user['user']['first_name'])
        self.assertTrue('last_name' in created_user and created_user['last_name'] == new_user['user']['last_name'])
        self.assertTrue('email' in created_user and created_user['email'] == new_user['user']['email'])

    def test_user_create_no_send_email_success(self):
        login_response = self.client.post(reverse('user_login'), {'email':self.admin_user.get_username(), 'password':self.user_password})
        new_user = {
            'user': {
                'first_name':'fiddfrstvvv5', 
                'last_name':'lastvvfdvv5', 
                'email':'user456@smoothbenefits.com'
                },
            'company': self.normalize_key(1),
            'company_user_type': 'employee',
            'send_email': 'false',
            'create_docs': 'true',
            'fields':[
                {'company_name':'benefitmy'}, 
                {'position': 'Software Engineer'}]
        }
        response = self.client.post(reverse('all_users'), json.dumps(new_user), content_type='application/json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)
        created_user = json.loads(response.content)
        self.assertTrue('id' in created_user and created_user['id'])
        self.assertTrue('first_name' in created_user and created_user['first_name'] == new_user['user']['first_name'])
        self.assertTrue('last_name' in created_user and created_user['last_name'] == new_user['user']['last_name'])
        self.assertTrue('email' in created_user and created_user['email'] == new_user['user']['email'])

    def test_user_create_no_create_docs_success(self):
        login_response = self.client.post(reverse('user_login'), {'email':self.admin_user.get_username(), 'password':self.user_password})
        new_user = {
            'user': {
                'first_name':'fiddfrstvvv5', 
                'last_name':'lastvvfdvv5', 
                'email':'user456@smoothbenefits.com'
                },
            'company': self.normalize_key(1),
            'company_user_type': 'employee',
            'send_email': 'false',
            'create_docs': 'false'
        }
        response = self.client.post(reverse('all_users'), json.dumps(new_user), content_type='application/json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)
        created_user = json.loads(response.content)
        self.assertTrue('id' in created_user and created_user['id'])
        self.assertTrue('first_name' in created_user and created_user['first_name'] == new_user['user']['first_name'])
        self.assertTrue('last_name' in created_user and created_user['last_name'] == new_user['user']['last_name'])
        self.assertTrue('email' in created_user and created_user['email'] == new_user['user']['email'])


    def test_user_create_no_company(self):
        login_response = self.client.post(reverse('user_login'), {'email':self.admin_user.get_username(), 'password':self.user_password})
        new_user = {
            'user': {
                'first_name':'fiddfrstvvv5', 
                'last_name':'lastvvfdvv5', 
                'email':'user456@smoothbenefits.com'
                },
            'company_user_type': 'employee',
        }
        response = self.client.post(reverse('all_users'), json.dumps(new_user), content_type='application/json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, '')

    def test_user_create_no_company_user_type(self):
        login_response = self.client.post(reverse('user_login'), {'email':self.admin_user.get_username(), 'password':self.user_password})
        new_user = {
            'user': {
                'first_name':'fiddfrstvvv5', 
                'last_name':'lastvvfdvv5', 
                'email':'user456@smoothbenefits.com'
                },
            'company': self.normalize_key(1),
        }
        response = self.client.post(reverse('all_users'), json.dumps(new_user), content_type='application/json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, '')
        
    def test_user_create_non_existing_company(self):
        login_response = self.client.post(reverse('user_login'), {'email':self.admin_user.get_username(), 'password':self.user_password})
        new_user = {
            'user': {
                'first_name':'fiddfrstvvv5', 
                'last_name':'lastvvfdvv5', 
                'email':'user456@smoothbenefits.com'
                },
            'company': 300,
            'company_user_type': 'employee',
        }
        response = self.client.post(reverse('all_users'), json.dumps(new_user), content_type='application/json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)

    def test_user_create_conflict(self):
        login_response = self.client.post(reverse('user_login'), {'email':self.admin_user.get_username(), 'password':self.user_password})
        new_user = {
            'user': {
                'first_name':'fiddfrstvvv5', 
                'last_name':'lastvvfdvv5', 
                'email':'user3@benefitmy.com'
                },
            'company': self.normalize_key(1),
            'company_user_type': 'employee',
        }
        response = self.client.post(reverse('all_users'), json.dumps(new_user), content_type='application/json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.content, '')
