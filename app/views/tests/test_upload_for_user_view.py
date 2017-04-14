import json
from django.conf import settings
from django.test import TestCase
from django.core.urlresolvers import reverse
from view_test_base import ViewTestBase

class UploadForUserTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['23_auth_user',
                'upload',
                '49_period_definition',
                '10_company',
                '34_company_user',
                'upload_for_user']

    def test_get_upload_for_user_success(self):
        response = self.client.get(
            reverse('upload_for_user_api', kwargs={'user_id': self.normalize_key(3)}),
        )

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 1)
        upload_for_user = result[0]
        self.assertEqual(upload_for_user['user_for'], self.normalize_key(3))
        self.assertIn('upload', upload_for_user)
        upload = upload_for_user['upload']
        self.assertEqual(upload['id'], self.normalize_key(5))
        self.assertEqual(upload['S3'], 'https://benefitmy-dev-uploads.s3.amazonaws.com/Greencard.jpeg')
        self.assertEqual(upload['file_type'], 'image/jpeg')
        self.assertEqual(upload['file_name'], 'Greencard.jpeg')
        self.assertEqual(upload['company'], self.normalize_key(1))
        self.assertEqual(upload['user'], self.normalize_key(2))


    def test_get_upload_for_user_non_exist_user(self):
        response = self.client.get(
            reverse('upload_for_user_api', kwargs={'user_id': self.normalize_key(34565)}),
        )
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        upload_for_user = json.loads(response.content)
        self.assertEqual(len(upload_for_user), 0)

    def test_post_for_user_success(self):
        upload_data = {
            'upload': self.normalize_key(3),
        }
        response = self.client.post(
            reverse('upload_for_user_api', 
                    kwargs={'user_id': self.normalize_key(3)}),
            data=json.dumps(upload_data),
            content_type='application/json'
        )
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.content)
        self.assertIn('id', result)
        self.assertEqual(result['id'], self.normalize_key(3))
        self.assertEqual(result['user_for'], 3)
        self.assertEqual(result['upload'], 3)

    def test_post_upload_for_user_bad_user_fail(self):
        upload_data = {
            'upload': self.normalize_key(3),
        }
        response = self.client.post(
            reverse('upload_for_user_api', 
                    kwargs={'user_id': self.normalize_key(45543)}),
            data=json.dumps(upload_data),
            content_type='application/json'
        )
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)


    def test_post_upload_for_user_bad_upload_fail(self):
        upload_data = {
            'upload': self.normalize_key(3453),
        }
        response = self.client.post(
            reverse('upload_for_user_api', 
                    kwargs={'user_id': self.normalize_key(4)}),
            data=json.dumps(upload_data),
            content_type='application/json'
        )
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)

    def test_delete_upload_for_user_success(self):
        response = self.client.delete(
            reverse('upload_for_user_api',
                    kwargs={'user_id': self.normalize_key(3)}
            )
        )
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 204)


    def test_delete_upload_for_user_non_exist_user(self):
        response = self.client.delete(
            reverse('upload_for_user_api',
                    kwargs={'user_id': self.normalize_key(4343)}
            )
        )
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 204)
