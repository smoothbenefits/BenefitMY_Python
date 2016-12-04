from django.test import TestCase
from django.core.urlresolvers import reverse
from view_test_base import ViewTestBase
import json


class OpenEnrollmentDefinitionTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['10_company', '23_auth_user', '49_period_definition', 'open_enrollment_definition']

    def test_get_open_enrollment_definition_success(self):
        response = self.client.get(reverse('company_open_enrollment_api',
                                           kwargs={'comp_id': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertTrue('company' in result)
        self.assertEqual(result['company']['id'], self.normalize_key(1))
        self.assertEqual(result['start_month'], 2)
        self.assertEqual(result['start_day'], 23)
        self.assertEqual(result['end_month'], 3)
        self.assertEqual(result['end_day'], 1)

    def test_get_open_enrollment_definition_non_exists(self):
        response = self.client.get(reverse('company_open_enrollment_api',
                                           kwargs={'comp_id': self.normalize_key(6)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)

    def test_post_open_enrollment_definition_success(self):
        open_enrollment_definition_data = {
            'company': self.normalize_key(2),
            'start_month': 4,
            'start_day': 12,
            'end_month': 5,
            'end_day': 6
        }
        response = self.client.post(
            reverse('company_open_enrollment_api', kwargs={'comp_id': self.normalize_key(2)}),
            data=json.dumps(open_enrollment_definition_data),
            content_type='application/json'
        )
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.content)
        self.assertTrue('company' in result)
        self.assertEqual(result['company'], 2)
        self.assertEqual(result['start_month'], open_enrollment_definition_data['start_month'])
        self.assertEqual(result['start_day'], open_enrollment_definition_data['start_day'])
        self.assertEqual(result['end_month'], open_enrollment_definition_data['end_month'])
        self.assertEqual(result['end_day'], open_enrollment_definition_data['end_day'])

    def test_post_open_enrollment_definition_error(self):
        open_enrollment_definition_data = {
            'company': self.normalize_key(6),
            'start_month': 4,
            'start_day': 12,
            'end_month': 5,
            'end_day': 6
        }
        response = self.client.post(
            reverse('company_open_enrollment_api', kwargs={'comp_id': self.normalize_key(6)}),
            data=json.dumps(open_enrollment_definition_data),
            content_type='application/json'
        )
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)

    def test_post_open_enrollment_definition_violates_unique_constraint(self):
        open_enrollment_definition_data = {
            'company': self.normalize_key(1),
            'start_month': 4,
            'start_day': 12,
            'end_month': 5,
            'end_day': 6
        }
        response = self.client.post(
            reverse('company_open_enrollment_api', kwargs={'comp_id': self.normalize_key(1)}),
            data=json.dumps(open_enrollment_definition_data),
            content_type='application/json'
        )
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)

    def test_put_open_enrollment_definition_success(self):
        open_enrollment_definition_data = {
            'company': self.normalize_key(1),
            'start_month': 4,
            'start_day': 12,
            'end_month': 5,
            'end_day': 6
        }
        response = self.client.put(
            reverse('company_open_enrollment_api', kwargs={'comp_id': self.normalize_key(1)}),
            data=json.dumps(open_enrollment_definition_data),
            content_type='application/json'
        )
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertTrue('company' in result)
        self.assertEqual(result['company'], open_enrollment_definition_data['company'])
        self.assertEqual(result['start_month'], open_enrollment_definition_data['start_month'])
        self.assertEqual(result['start_day'], open_enrollment_definition_data['start_day'])
        self.assertEqual(result['end_month'], open_enrollment_definition_data['end_month'])
        self.assertEqual(result['end_day'], open_enrollment_definition_data['end_day'])

    def test_put_open_enrollment_definition_non_exist(self):
        open_enrollment_definition_data = {
            'company': self.normalize_key(6),
            'start_month': 4,
            'start_day': 12,
            'end_month': 5,
            'end_day': 6
        }
        response = self.client.put(
            reverse('company_open_enrollment_api', kwargs={'comp_id': self.normalize_key(6)}),
            data=json.dumps(open_enrollment_definition_data),
            content_type='application/json'
        )
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)

    def test_delete_open_enrollment_definition_success(self):
        response = self.client.delete(reverse('company_open_enrollment_api',
                                           kwargs={'comp_id': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 204)

        response = self.client.get(reverse('company_open_enrollment_api',
                                           kwargs={'comp_id': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)

    def test_delete_open_enrollment_definition_non_exists(self):
        response = self.client.delete(reverse('company_open_enrollment_api',
                                           kwargs={'comp_id': self.normalize_key(6)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)
