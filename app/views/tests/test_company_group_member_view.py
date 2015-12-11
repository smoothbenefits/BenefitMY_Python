from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import MULTIPART_CONTENT
from view_test_base import ViewTestBase
import json


class CompanyGroupMemberTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['49_period_definition', '10_company', '61_company_group', '62_company_group_member', '23_auth_user']

    def test_get_company_group_member_by_company_group_success(self):
        response = self.client.get(reverse('company_group_company_group_member_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertEqual(2, len(result))

        result = sorted(result, key=lambda x: x['id'])
        self.assertIn('user', result[0])
        self.assertEqual(result[0]['user']['id'], self.normalize_key(3))
        self.assertEqual(result[0]['user']['first_name'], 'Simon')
        self.assertEqual(result[0]['user']['last_name'], 'Cowell')
        self.assertEqual(result[0]['user']['email'], 'user3@benefitmy.com')
        self.assertIn('company_group', result[0])
        self.assertEqual(result[0]['company_group']['id'], self.normalize_key(1))
        self.assertEqual(result[0]['company_group']['name'], 'Management')
        self.assertIn('user', result[1])
        self.assertEqual(result[1]['user']['id'], self.normalize_key(4))
        self.assertEqual(result[1]['user']['first_name'], 'Jenn')
        self.assertEqual(result[1]['user']['last_name'], 'Glovorski')
        self.assertEqual(result[1]['user']['email'], 'user4@benefitmy.com')
        self.assertIn('company_group', result[1])
        self.assertEqual(result[1]['company_group']['id'], self.normalize_key(1))
        self.assertEqual(result[1]['company_group']['name'], 'Management')

    def test_get_company_group_member_by_company_group_non_exist(self):
        response = self.client.get(reverse('company_group_company_group_member_api',
                                           kwargs={'pk': self.normalize_key(23)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertEqual(0, len(result))


    def test_post_company_group_member(self):
        post_data = {
            "company_group": self.normalize_key(2),
            "user": self.normalize_key(7)
        }
        response = self.client.post(reverse('company_group_member_api',
                                    kwargs={'pk': self.normalize_key(1)}),
                                    data=json.dumps(post_data),
                                    content_type='application/json')

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.content)
        self.assertIn('id', result)
        self.assertEqual(result['id'], self.normalize_key(3))
        self.assertIn('user', result)
        self.assertEqual(result['user'], 7)
        self.assertIn('company_group', result)
        self.assertEqual(result['company_group'], 2)

    def test_post_company_group_member_bad_data(self):
        post_data = {
            "company_group": self.normalize_key(12),
            "user": self.normalize_key(7)
        }
        response = self.client.post(reverse('company_group_member_api',
                                    kwargs={'pk': self.normalize_key(1)}),
                                    data=json.dumps(post_data),
                                    content_type='application/json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)

    def test_put_company_group_member(self):
        put_data = {
            "company_group": self.normalize_key(2),
            "user": self.normalize_key(4)
        }
        response = self.client.put(reverse('company_group_member_api',
                                   kwargs={'pk': self.normalize_key(2)}),
                                   data=json.dumps(put_data),
                                   content_type='application/json')

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertIn('id', result)
        self.assertEqual(result['id'], self.normalize_key(2))
        self.assertIn('user', result)
        self.assertEqual(result['user'], self.normalize_key(4))
        self.assertIn('company_group', result)
        self.assertEqual(result['company_group'], self.normalize_key(2))

    def test_put_company_group_member_non_exist(self):
        put_data = {
            "company_group": self.normalize_key(2),
            "user": self.normalize_key(4)
        }
        response = self.client.put(reverse('company_group_member_api',
                                   kwargs={'pk': self.normalize_key(12)}),
                                   data=json.dumps(put_data),
                                   content_type='application/json')

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)

    def test_delete_company_group_member(self):
        response = self.client.delete(reverse('company_group_member_api',
                                    kwargs={'pk': self.normalize_key(2)}),
                                    content_type='application/json')

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 204)

        response = self.client.get(reverse('company_group_company_group_member_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertEqual(1, len(result))
        self.assertIn('user', result[0])
        self.assertEqual(result[0]['user']['id'], self.normalize_key(3))
        self.assertEqual(result[0]['user']['first_name'], 'Simon')
        self.assertEqual(result[0]['user']['last_name'], 'Cowell')
        self.assertEqual(result[0]['user']['email'], 'user3@benefitmy.com')
        self.assertIn('company_group', result[0])
        self.assertEqual(result[0]['company_group']['id'], self.normalize_key(1))
        self.assertEqual(result[0]['company_group']['name'], 'Management')

    def test_delete_company_group_member_non_exist(self):
        response = self.client.delete(reverse('company_group_member_api',
                                    kwargs={'pk': self.normalize_key(12)}),
                                    content_type='application/json')

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)

    def test_get_company_group_member_by_company_success(self):
        response = self.client.get(reverse('company_group_member_company_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertEqual(3, len(result))

        result = sorted(result, key=lambda x: x['id'])
        group = result[0]
        self.assertEqual(group['id'], self.normalize_key(1))
        self.assertEqual(group['name'], 'Management')
        self.assertEqual(group['company']['id'], self.normalize_key(1))
        members = group['company_group_members']
        self.assertEqual(len(members), 2)
        members = sorted(members, key=lambda x: x['id'])
        self.assertEqual(members[0]['id'], self.normalize_key(1))
        self.assertEqual(members[0]['user']['id'], self.normalize_key(3))
        self.assertEqual(members[1]['id'], self.normalize_key(2))
        self.assertEqual(members[1]['user']['id'], self.normalize_key(4))
        group = result[1]
        self.assertEqual(group['id'], self.normalize_key(2))
        self.assertEqual(group['name'], 'Salary-based')
        self.assertEqual(group['company']['id'], self.normalize_key(1))
        self.assertEqual(group['company_group_members'], [])
        group = result[2]
        self.assertEqual(group['id'], self.normalize_key(3))
        self.assertEqual(group['name'], 'Contractor')
        self.assertEqual(group['company']['id'], self.normalize_key(1))
        self.assertEqual(group['company_group_members'], [])

def test_get_company_group_member_by_company_non_exist(self):
        response = self.client.get(reverse('company_group_member_company_api',
                                           kwargs={'pk': self.normalize_key(11)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)


