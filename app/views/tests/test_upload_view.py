import json
from django.conf import settings
from django.test import TestCase
from django.core.urlresolvers import reverse
from view_test_base import ViewTestBase


class UploadTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['23_auth_user', 'upload', '10_company']

    def setUp(self):
        self.upload_data = {
            'company': 1,
            'user': 4,
            'upload_type': 'I9',
            'file_name': 'tester.pdf',
            'file_type': 'application/pdf',
            'company_name': 'carbonite',
        }

    def test_get_uploads_by_user_success(self):
        response = self.client.get(reverse('uploads_by_user',
                                           kwargs={'pk': self.normalize_key(3)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 2)
        upload1 = None
        for x in result:
            if x['id'] == self.normalize_key(1):
                upload1 = x
                break
        self.assertEqual(upload1['S3'], 'https://benefitmy-dev-uploads.s3.amazonaws.com/user_id_3_company_id_1_passport.jpg')
        self.assertEqual(upload1['file_type'], 'image/jpeg')
        self.assertEqual(upload1['file_name'], 'passport.jpg')
        self.assertEqual(upload1['company'], self.normalize_key(1))
        self.assertEqual(upload1['user'], self.normalize_key(3))
        self.assertEqual(upload1['id'], self.normalize_key(1))
        self.assertEqual(upload1['upload_type'], 'I9')
        upload2 = None
        for x in result:
            if x['id'] == self.normalize_key(2):
                upload2 = x
                break
        self.assertEqual(upload2['S3'], 'https://benefitmy-dev-uploads.s3.amazonaws.com/user_id_3_company_id_1_driverlicense.png')
        self.assertEqual(upload2['file_type'], 'image/png')
        self.assertEqual(upload2['file_name'], 'driverlicense.png')
        self.assertEqual(upload2['company'], self.normalize_key(1))
        self.assertEqual(upload2['user'], self.normalize_key(3))
        self.assertEqual(upload2['id'], self.normalize_key(2))
        self.assertEqual(upload2['upload_type'], 'I9')

    def test_get_uploads_by_user_empty(self):
        response = self.client.get(reverse('uploads_by_user',
                                           kwargs={'pk': self.normalize_key(2)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)
        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 0)


    def test_get_upload_by_user_non_exist_user(self):
        response = self.client.get(reverse('uploads_by_user',
                                           kwargs={'pk': self.normalize_key(144)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)
        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 0)


    def test_post_upload_success(self):
        response = self.client.post(reverse('uploads_by_user',
                                           kwargs={'pk': self.normalize_key(4)}),
                                    data=self.upload_data)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.content)
        self.assertTrue('S3' in result)
        self.assertIsNotNone(result['S3'])
        self.assertEqual(result['file_type'], self.upload_data['file_type'])
        self.assertEqual(result['file_name'], self.upload_data['file_name'])
        self.assertEqual(result['company'], 1)
        self.assertEqual(result['user'], 4)
        self.assertEqual(result['id'], self.normalize_key(4))
        self.assertEqual(result['upload_type'], self.upload_data['upload_type'])
        self.assertTrue('s3Host' in result)
        self.assertEqual(result['s3Host'], settings.AMAZON_S3_HOST)
        self.assertTrue('policy' in result)
        self.assertIsNotNone(result['policy'])
        self.assertTrue('signature' in result)
        self.assertIsNotNone(result['signature'])
        self.assertTrue('fileKey'in result)
        self.assertIsNotNone(result['fileKey'])
        self.assertEqual(result['accessKey'], settings.AMAZON_AWS_ACCESS_KEY_ID)

        response = self.client.get(reverse('uploads_by_user',
                                           kwargs={'pk': self.normalize_key(4)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 2)
        upload1 = None
        for x in result:
            if x['id'] == self.normalize_key(3):
                upload1 = x
                break
        self.assertEqual(upload1['S3'], 'https://benefitmy-dev-uploads.s3.amazonaws.com/user_id_4_company_id_1_I94.jpg')
        self.assertEqual(upload1['file_type'], 'application/pdf')
        self.assertEqual(upload1['file_name'], 'I94.pdf')
        self.assertEqual(upload1['company'], self.normalize_key(1))
        self.assertEqual(upload1['user'], self.normalize_key(4))
        self.assertEqual(upload1['id'], self.normalize_key(3))
        self.assertEqual(upload1['upload_type'], 'I9')
        upload2 = None
        for x in result:
            if x['id'] == self.normalize_key(4):
                upload2 = x
                break
        self.assertIsNotNone(upload2['S3'])
        self.assertEqual(upload2['file_type'], self.upload_data['file_type'])
        self.assertEqual(upload2['file_name'], self.upload_data['file_name'])
        self.assertEqual(upload2['company'], self.normalize_key(1))
        self.assertEqual(upload2['user'], self.normalize_key(4))
        self.assertEqual(upload2['id'], self.normalize_key(4))
        self.assertEqual(upload2['upload_type'], self.upload_data['upload_type'])

    def test_upload_post_with_non_exist_user(self):
        self.upload_data.update({'user': 128})
        response = self.client.post(reverse('uploads_by_user',
                                           kwargs={'pk': self.normalize_key(4)}),
                                    data=self.upload_data)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)
        self.assertIsNotNone(response.content)


    def test_upload_post_with_non_exist_company(self):
        self.upload_data.update({'company': 122})
        response = self.client.post(reverse('uploads_by_user',
                                           kwargs={'pk': self.normalize_key(4)}),
                                    data=self.upload_data)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)
        self.assertIsNotNone(response.content)

    def test_delete_upload_success(self):
        response = self.client.delete(reverse('upload_api',
                                           kwargs={'pk': self.normalize_key(2)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertTrue('auth' in result)
        self.assertIsNotNone(result['auth'])
        self.assertTrue('S3' in result)
        self.assertIsNotNone(result['S3'])
        self.assertTrue('time' in result)

        response = self.client.get(reverse('uploads_by_user',
                                           kwargs={'pk': self.normalize_key(3)}))

        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 1)
        upload1 = result[0]
        self.assertEqual(upload1['S3'], 'https://benefitmy-dev-uploads.s3.amazonaws.com/user_id_3_company_id_1_passport.jpg')
        self.assertEqual(upload1['file_type'], 'image/jpeg')
        self.assertEqual(upload1['file_name'], 'passport.jpg')
        self.assertEqual(upload1['company'], self.normalize_key(1))
        self.assertEqual(upload1['user'], self.normalize_key(3))
        self.assertEqual(upload1['id'], self.normalize_key(1))
        self.assertEqual(upload1['upload_type'], 'I9')

    def test_delete_upload_non_exist(self):
        response = self.client.delete(reverse('upload_api',
                                           kwargs={'pk': self.normalize_key(78)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)
        self.assertIsNotNone(response.content)
        

    def test_get_by_id_success(self):
        response = self.client.get(reverse('upload_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        upload1 = json.loads(response.content)
        self.assertEqual(upload1['S3'], 'https://benefitmy-dev-uploads.s3.amazonaws.com/user_id_3_company_id_1_passport.jpg')
        self.assertEqual(upload1['file_type'], 'image/jpeg')
        self.assertEqual(upload1['file_name'], 'passport.jpg')
        self.assertEqual(upload1['company'], self.normalize_key(1))
        self.assertEqual(upload1['user'], self.normalize_key(3))
        self.assertEqual(upload1['id'], self.normalize_key(1))
        self.assertEqual(upload1['upload_type'], 'I9')

    def test_get_by_id_non_exist(self):
        response = self.client.get(reverse('upload_api',
                                           kwargs={'pk': self.normalize_key(90)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)
        self.assertIsNotNone(response.content)
