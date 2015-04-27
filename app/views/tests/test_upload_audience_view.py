import json
from django.conf import settings
from django.test import TestCase
from django.core.urlresolvers import reverse
from view_test_base import ViewTestBase

class UploadAudienceTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['23_auth_user', 
                'upload', 
                '10_company', 
                '34_company_user', 
                'upload_audience']        

    def test_get_upload_audience_company_success(self):
        response = self.client.get(reverse('upload_audience_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 1)
        upload_audience = result[0]
        self.assertIn('company', upload_audience)
        target_company = upload_audience['company']
        self.assertEqual(target_company['id'], self.normalize_key(1))
        self.assertEqual(target_company['name'], 'BenefitMy Inc.')
        self.assertIn('upload', upload_audience)
        upload = upload_audience['upload']
        self.assertEqual(upload['id'], self.normalize_key(6))
        self.assertEqual(upload['S3'], 'https://benefitmy-dev-uploads.s3.amazonaws.com/401KPolicy.pdf')
        self.assertEqual(upload['file_type'], 'application/pdf')
        self.assertEqual(upload['file_name'], '401KPolicy.pdf')
        self.assertEqual(upload['company'], self.normalize_key(1))
        self.assertEqual(upload['user'], self.normalize_key(2))
        self.assertEqual(upload['upload_type'], 'Manager')

    def test_get_upload_audience_user_success(self):
        response = self.client.get("{0}?user_id={1}".format(
                                       reverse('upload_audience_api',
                                           kwargs={'pk': self.normalize_key(1)}), 
                                       self.normalize_key(3)))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 1)
        upload_audience = result[0]
        self.assertEqual(upload_audience['user_for'], self.normalize_key(3))
        self.assertIn('company', upload_audience)
        target_company = upload_audience['company']
        self.assertEqual(target_company['id'], self.normalize_key(1))
        self.assertEqual(target_company['name'], 'BenefitMy Inc.')
        self.assertIn('upload', upload_audience)
        upload = upload_audience['upload']
        self.assertEqual(upload['id'], self.normalize_key(5))
        self.assertEqual(upload['S3'], 'https://benefitmy-dev-uploads.s3.amazonaws.com/Greencard.jpeg')
        self.assertEqual(upload['file_type'], 'image/jpeg')
        self.assertEqual(upload['file_name'], 'Greencard.jpeg')
        self.assertEqual(upload['company'], self.normalize_key(1))
        self.assertEqual(upload['user'], self.normalize_key(2))
        self.assertEqual(upload['upload_type'], 'I9')

    