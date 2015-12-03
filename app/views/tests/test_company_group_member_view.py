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
