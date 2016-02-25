import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from app.views.tests.view_test_base import ViewTestBase


class UserOnboardingStepStateViewTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['23_auth_user', '72_user_onboarding_step_state']

    def test_get_step_state_entry_success(self):
        response = self.client.get(reverse('user_onboarding_step_states_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['user'], self.normalize_key(2))
        self.assertEqual(result['step'], 'direct_deposit')
        self.assertEqual(result['state'], 'skipped')

    def test_create_step_state_entry_success(self):
        post_data = {'user': self.normalize_key(3),
                    'step': 'direct_deposit',
                    'state': 'completed'}
        response = self.client.post(reverse('user_onboarding_step_states_post_api'),
                                           json.dumps(post_data),
                                           content_type='application/json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)

        response = self.client.get(reverse('user_onboarding_step_states_api',
                                           kwargs={'pk': self.normalize_key(2)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['user'], self.normalize_key(3))
        self.assertEqual(result['step'], 'direct_deposit')
        self.assertEqual(result['state'], 'completed')

    def test_create_step_state_entry_duplicate_user_step_failure(self):
        post_data = {'user': self.normalize_key(2),
                    'step': 'direct_deposit',
                    'state': 'completed'}
        response = self.client.post(reverse('user_onboarding_step_states_post_api'),
                                           json.dumps(post_data),
                                           content_type='application/json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)

    def test_update_step_state_entry_success(self):
        post_data = {'id': self.normalize_key(1),
                    'user': self.normalize_key(2),
                    'step': 'direct_deposit',
                    'state': 'completed'}
        response = self.client.put(reverse('user_onboarding_step_states_api',
                                            kwargs={'pk': self.normalize_key(1)}),
                                           json.dumps(post_data),
                                           content_type='application/json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('user_onboarding_step_states_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['user'], self.normalize_key(2))
        self.assertEqual(result['step'], 'direct_deposit')
        self.assertEqual(result['state'], 'completed')

    def test_get_step_state_entry_by_user_success(self):
        response = self.client.get(reverse('user_onboarding_step_states_by_user_api',
                                           kwargs={'pk': self.normalize_key(2)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['user'], self.normalize_key(2))
        self.assertEqual(result[0]['step'], 'direct_deposit')
        self.assertEqual(result[0]['state'], 'skipped')
