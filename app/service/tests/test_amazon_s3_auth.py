import base64
import hmac, hashlib
import json
from django.conf import settings
from django.test import TestCase
from app.service.amazon_s3_auth import AmazonS3AuthService
# Create your tests here.
class TestAmazonS3AuthService(TestCase):
    def setUp(self):
        self.auth_service = AmazonS3AuthService()
        self.test_data = {
            'company': 1,
            'user': 4,
            'upload_type': 'I9',
            'file_name': 'tester.pdf',
            'file_type': 'application/pdf',
            'company_name': 'carbonite',
        }

    def test_encode_key(self):
        file_key = self.auth_service.encode_key(self.test_data['company'], self.test_data['user'])
        file_key_decoded = base64.b64decode(file_key)
        self.assertTrue(str(self.test_data['company']) in file_key_decoded)
        self.assertTrue(str(self.test_data['user']) in file_key_decoded)


    def test_get_s3_key(self):
        file_key = self.auth_service.encode_key(self.test_data['company'], self.test_data['user'])
        s3_key = self.auth_service.get_s3_key(self.test_data['company_name'],
                                              self.test_data['file_name'],
                                              file_key)
        file_elements = s3_key.split(":")
        self.assertEqual(file_elements[0], self.test_data['company_name'])
        self.assertEqual(file_elements[1], file_key)
        self.assertEqual(file_elements[2], self.test_data['file_name'])


    def test_get_upload_form_policy_and_signature(self):
        file_key = self.auth_service.encode_key(self.test_data['company'], self.test_data['user'])
        s3_key = self.auth_service.get_s3_key(self.test_data['company_name'],
                                              self.test_data['file_name'],
                                              file_key)
        s3_info = self.auth_service.get_upload_form_policy_and_signature(s3_key)
        self.assertIsNotNone(s3_info['signature'])
        self.assertEqual(s3_info['s3Host'], settings.AMAZON_S3_HOST)
        self.assertEqual(s3_info['accessKey'], settings.AMAZON_AWS_ACCESS_KEY_ID)
        self.assertEqual(s3_info['fileKey'], s3_key)
        policy_item = s3_info['policy']
        decoded_policy_item = base64.b64decode(policy_item)
        raw_policy_item = json.loads(decoded_policy_item)
        self.assertEqual(raw_policy_item['conditions'], settings.AMAZON_S3_UPLOAD_POLICY['conditions'])


    def test_get_s3_request_datetime(self):
        request_datetime = self.auth_service.get_s3_request_datetime()
        self.assertIsNotNone(request_datetime)


    def test_get_s3_request_auth(self):
        cur_time = self.auth_service.get_s3_request_datetime()
        request_auth = self.auth_service.get_s3_request_auth("DELETE", "", "haha", cur_time)
        auth_array_1 = request_auth.split(" ")
        self.assertEqual(len(auth_array_1), 2)
        self.assertEqual(auth_array_1[0], "AWS")
        auth_array_2 = auth_array_1[1].split(":")
        self.assertEqual(len(auth_array_2), 2)
        self.assertEqual(auth_array_2[0], settings.AMAZON_AWS_ACCESS_KEY_ID)
        self.assertIsNotNone(auth_array_2[1])
