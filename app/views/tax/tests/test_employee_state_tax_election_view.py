import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from app.views.tests.view_test_base import ViewTestBase


class EmployeeStateTaxElectionTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['84_employee_state_tax_election',
                '49_period_definition', '10_company',
                '24_person', '23_auth_user']

    def test__get_employee_state_tax_election__exists__success(self):
        response = self.client.get(reverse('employee_state_tax_election_api',
                                           kwargs={
                                                'user_id': self.normalize_key(3),
                                                'state': 'MA'}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['user'], self.normalize_key(3))
        self.assertEqual(result['state'], 'MA')
        self.assertIsNotNone(result['tax_election_data'])

    def test__get_employee_state_tax_election__not_exists__404(self):
        response = self.client.get(reverse('employee_state_tax_election_api',
                                           kwargs={
                                                'user_id': self.normalize_key(4),
                                                'state': 'MA'}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)

    def test__delete_employee_state_tax_election__exists__success(self):
        response = self.client.get(reverse('employee_state_tax_election_api',
                                           kwargs={
                                                'user_id': self.normalize_key(3),
                                                'state': 'MA'}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        response = self.client.delete(reverse('employee_state_tax_election_api',
                                           kwargs={
                                                'user_id': self.normalize_key(3),
                                                'state': 'MA'}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 204)

        response = self.client.get(reverse('employee_state_tax_election_api',
                                           kwargs={
                                                'user_id': self.normalize_key(3),
                                                'state': 'MA'}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)

    def test__post_employee_state_tax_election__not_exists_with_valid_data__success(self):
        post_data = {
            "user": "4", 
            "tax_election_data": {
                "personal_exemption": 1,
                "spouse_exemption": 4,
                "num_dependents": 0,
                "additional_witholding": 11.1,
                "head_of_household": True,
                "is_blind": False,
                "is_spouse_blind": False,
                "is_fulltime_student": False
            }, 
            "state": "MA"
        }

        # Verify that the state election for the user does not exist
        response = self.client.get(reverse('employee_state_tax_election_api',
                                           kwargs={
                                                'user_id': self.normalize_key(4),
                                                'state': 'MA'}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)

        # Now do the POST
        response = self.client.post(reverse('employee_state_tax_election_api',
                                           kwargs={
                                                'user_id': self.normalize_key(4),
                                                'state': 'MA'}),
                                    data=json.dumps(post_data),
                                    content_type='application/json')

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)

        # Now validate the POST result
        response = self.client.get(reverse('employee_state_tax_election_api',
                                           kwargs={
                                                'user_id': self.normalize_key(4),
                                                'state': 'MA'}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['user'], self.normalize_key(4))
        self.assertEqual(result['state'], 'MA')
        self.assertIsNotNone(result['tax_election_data'])
        self.assertEqual(result['tax_election_data']['personal_exemption'], post_data['tax_election_data']['personal_exemption'])
        self.assertEqual(float(result['tax_election_data']['additional_witholding']), float(post_data['tax_election_data']['additional_witholding']))

    def test__post_employee_state_tax_election__exists_with_valid_data__400(self):
        post_data = {
            "user": "3", 
            "tax_election_data": {
                "personal_exemption": 1,
                "spouse_exemption": 4,
                "num_dependents": 0,
                "additional_witholding": 11.1,
                "head_of_household": True,
                "is_blind": False,
                "is_spouse_blind": False,
                "is_fulltime_student": False
            }, 
            "state": "MA"
        }

        # Verify that the state election for the user already exists
        response = self.client.get(reverse('employee_state_tax_election_api',
                                           kwargs={
                                                'user_id': self.normalize_key(3),
                                                'state': 'MA'}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        # Now do the POST
        response = self.client.post(reverse('employee_state_tax_election_api',
                                           kwargs={
                                                'user_id': self.normalize_key(3),
                                                'state': 'MA'}),
                                    data=json.dumps(post_data),
                                    content_type='application/json')

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)

    def test__post_employee_state_tax_election__not_exists_with_invalid_data__400(self):
        post_data = {
            "user": "4", 
            "tax_election_data": {
                # Note the missing of the required field "personal_exemption"
                # "personal_exemption": 1,
                "spouse_exemption": 4,
                "num_dependents": 0,
                "additional_witholding": 11.1,
                "head_of_household": True,
                "is_blind": False,
                "is_spouse_blind": False,
                "is_fulltime_student": False
            }, 
            "state": "MA"
        }

        # Verify that the state election for the user does not exist
        response = self.client.get(reverse('employee_state_tax_election_api',
                                           kwargs={
                                                'user_id': self.normalize_key(4),
                                                'state': 'MA'}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)

        # Now do the POST
        response = self.client.post(reverse('employee_state_tax_election_api',
                                           kwargs={
                                                'user_id': self.normalize_key(4),
                                                'state': 'MA'}),
                                    data=json.dumps(post_data),
                                    content_type='application/json')

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)

    def test__put_employee_state_tax_election__exists_with_valid_data__success(self):
        post_data = {
            "user": "3", 
            "tax_election_data": {
                "personal_exemption": 1,
                "spouse_exemption": 4,
                "num_dependents": 0,
                "additional_witholding": 22.22,
                "head_of_household": True,
                "is_blind": False,
                "is_spouse_blind": False,
                "is_fulltime_student": True
            }, 
            "state": "MA"
        }

        # Verify that the state election for the user exists
        response = self.client.get(reverse('employee_state_tax_election_api',
                                           kwargs={
                                                'user_id': self.normalize_key(3),
                                                'state': 'MA'}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        # Now do the PUT
        response = self.client.put(reverse('employee_state_tax_election_api',
                                           kwargs={
                                                'user_id': self.normalize_key(3),
                                                'state': 'MA'}),
                                    data=json.dumps(post_data),
                                    content_type='application/json')

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        # Now validate the PUT result
        response = self.client.get(reverse('employee_state_tax_election_api',
                                           kwargs={
                                                'user_id': self.normalize_key(3),
                                                'state': 'MA'}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['user'], self.normalize_key(3))
        self.assertEqual(result['state'], 'MA')
        self.assertIsNotNone(result['tax_election_data'])
        self.assertEqual(result['tax_election_data']['personal_exemption'], post_data['tax_election_data']['personal_exemption'])
        self.assertEqual(float(result['tax_election_data']['additional_witholding']), float(post_data['tax_election_data']['additional_witholding']))

    def test__put_employee_state_tax_election__not_exists_with_valid_data__404(self):
        post_data = {
            "user": "4", 
            "tax_election_data": {
                "personal_exemption": 1,
                "spouse_exemption": 4,
                "num_dependents": 0,
                "additional_witholding": 22.22,
                "head_of_household": True,
                "is_blind": False,
                "is_spouse_blind": False,
                "is_fulltime_student": True
            }, 
            "state": "MA"
        }

        # Verify that the state election for the user exists
        response = self.client.get(reverse('employee_state_tax_election_api',
                                           kwargs={
                                                'user_id': self.normalize_key(4),
                                                'state': 'MA'}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)

        # Now do the PUT
        response = self.client.put(reverse('employee_state_tax_election_api',
                                           kwargs={
                                                'user_id': self.normalize_key(4),
                                                'state': 'MA'}),
                                    data=json.dumps(post_data),
                                    content_type='application/json')

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)

    def test__put_employee_state_tax_election__exists_with_invalid_data__400(self):
        post_data = {
            "user": "3", 
            "tax_election_data": {
                # Note the missing of the required field "personal_exemption"
                # "personal_exemption": 1,
                "spouse_exemption": 4,
                "num_dependents": 0,
                "additional_witholding": 22.22,
                "head_of_household": True,
                "is_blind": False,
                "is_spouse_blind": False,
                "is_fulltime_student": True
            }, 
            "state": "MA"
        }

        # Verify that the state election for the user exists
        response = self.client.get(reverse('employee_state_tax_election_api',
                                           kwargs={
                                                'user_id': self.normalize_key(3),
                                                'state': 'MA'}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        # Now do the PUT
        response = self.client.put(reverse('employee_state_tax_election_api',
                                           kwargs={
                                                'user_id': self.normalize_key(3),
                                                'state': 'MA'}),
                                    data=json.dumps(post_data),
                                    content_type='application/json')

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)

    def test__get_employee_state_tax_election_by_employee__exists__success(self):
        response = self.client.get(reverse('employee_state_tax_election_by_employee_api',
                                           kwargs={'user_id': self.normalize_key(3)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 2)
