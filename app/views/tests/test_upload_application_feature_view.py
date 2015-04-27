import json
from django.conf import settings
from django.test import TestCase
from django.core.urlresolvers import reverse
from view_test_base import ViewTestBase

class UploadApplicationFeatureTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['23_auth_user', 
                'upload', 
                '10_company', 
                '34_company_user', 
                'sys_application_feature', 
                'upload_application_feature']        

    def test_get_upload_application_feature_success(self):
        response = self.client.get(reverse('uploads_application_feature_api',
                                           kwargs={'pk': self.normalize_key(3),
                                                   'feature_id': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 1)
        upload_feature = result[0]
        self.assertEqual(upload_feature['id'], self.normalize_key(1))
        self.assertEqual(upload_feature['feature_id'], self.normalize_key(1))
        self.assertIn('upload', upload_feature)
        upload = upload_feature['upload']
        self.assertEqual(upload['id'], self.normalize_key(4))
        self.assertEqual(upload['S3'], 'https://benefitmy-dev-uploads.s3.amazonaws.com/BSBCHMOSummary.pdf')
        self.assertEqual(upload['file_type'], 'application/pdf')
        self.assertEqual(upload['file_name'], 'BSBCHMOSummary.pdf')
        self.assertEqual(upload['company'], self.normalize_key(1))
        self.assertEqual(upload['user'], self.normalize_key(1))
        self.assertEqual(upload['upload_type'], 'MedicalBenefit')
        self.assertIn('application_feature', upload_feature)
        feature_type = upload_feature['application_feature']
        self.assertEqual(feature_type['id'], self.normalize_key(3))
        self.assertEqual(feature_type['feature'], 'MedicalBenefitPlan')

    def test_get_upload_application_feature_non_exists(self):
        response = self.client.get(reverse('uploads_application_feature_api',
                                           kwargs={'pk': self.normalize_key(887),
                                                   'feature_id': self.normalize_key(3)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        upload_features = json.loads(response.content)
        self.assertEqual(len(upload_features), 0)

    def test_get_upload_application_feature_no_such_feature(self):
        response = self.client.get(reverse('uploads_application_feature_api',
                                           kwargs={'pk': self.normalize_key(3),
                                                   'feature_id': self.normalize_key(120)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        upload_features = json.loads(response.content)
        self.assertEqual(len(upload_features), 0)

    def test_post_upload_application_feature_success(self):
        upload_feature_data = {
            'upload': self.normalize_key(3),
        }
        response = self.client.post(reverse('uploads_application_feature_api',
                                           kwargs={'pk': self.normalize_key(3),
                                                   'feature_id': self.normalize_key(2)}),
                                    data=json.dumps(upload_feature_data),
                                    content_type='application/json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.content)
        self.assertIn('id', result)
        self.assertEqual(result['id'], self.normalize_key(2))
        self.assertEqual(result['application_feature'], 3)
        self.assertEqual(result['feature_id'], 2)
        self.assertEqual(result['upload'], 3)

    def test_post_upload_application_feature_fail_bad_upload_data(self):
        upload_feature_data = {
            'upload': self.normalize_key(123),
        }
        response = self.client.post(reverse('uploads_application_feature_api',
                                           kwargs={'pk': self.normalize_key(3),
                                                   'feature_id': self.normalize_key(2)}),
                                    data=json.dumps(upload_feature_data),
                                    content_type='application/json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)
    
    def test_post_upload_application_feature_fail_bad_application_feature(self):
        upload_feature_data = {
            'upload': self.normalize_key(2),
        }
        response = self.client.post(reverse('uploads_application_feature_api',
                                           kwargs={'pk': self.normalize_key(356),
                                                   'feature_id': self.normalize_key(2)}),
                                    data=json.dumps(upload_feature_data),
                                    content_type='application/json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)

    def test_post_upload_application_feature_success_bad_feature_id(self):
        upload_feature_data = {
            'upload': self.normalize_key(3),
        }
        response = self.client.post(reverse('uploads_application_feature_api',
                                           kwargs={'pk': self.normalize_key(3),
                                                   'feature_id': self.normalize_key(4554)}),
                                    data=json.dumps(upload_feature_data),
                                    content_type='application/json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.content)
        self.assertIn('id', result)
        self.assertEqual(result['id'], self.normalize_key(2))
        self.assertEqual(result['application_feature'], 3)
        self.assertEqual(result['feature_id'], 4554)
        self.assertEqual(result['upload'], 3)

    def test_delete_upload_application_feature_success(self):
        upload_feature_data = {
            'upload': self.normalize_key(4),
        }
        response = self.client.post(reverse('uploads_application_feature_api',
                                           kwargs={'pk': self.normalize_key(3),
                                                   'feature_id': self.normalize_key(4554)}),
                                    data=json.dumps(upload_feature_data),
                                    content_type='application/json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)

        response = self.client.get(reverse('uploads_application_feature_api',
                                           kwargs={'pk': self.normalize_key(3),
                                                   'feature_id': self.normalize_key(4554)}))
        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 1)
        upload_feature = result[0]
        self.assertEqual(upload_feature['feature_id'], self.normalize_key(4554))
        self.assertIn('upload', upload_feature)
        upload = upload_feature['upload']
        self.assertEqual(upload['id'], self.normalize_key(4))
        self.assertEqual(upload['S3'], 'https://benefitmy-dev-uploads.s3.amazonaws.com/BSBCHMOSummary.pdf')
        self.assertEqual(upload['file_type'], 'application/pdf')
        self.assertEqual(upload['file_name'], 'BSBCHMOSummary.pdf')
        self.assertEqual(upload['company'], self.normalize_key(1))
        self.assertEqual(upload['user'], self.normalize_key(1))
        self.assertEqual(upload['upload_type'], 'MedicalBenefit')
        self.assertIn('application_feature', upload_feature)
        feature_type = upload_feature['application_feature']
        self.assertEqual(feature_type['id'], self.normalize_key(3))
        self.assertEqual(feature_type['feature'], 'MedicalBenefitPlan')

        response = self.client.delete(reverse('uploads_application_feature_api',
                                           kwargs={'pk': self.normalize_key(3),
                                                   'feature_id': self.normalize_key(4554)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 204)

        response = self.client.get(reverse('uploads_application_feature_api',
                                           kwargs={'pk': self.normalize_key(3),
                                                   'feature_id': self.normalize_key(4554)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        upload_features = json.loads(response.content)
        self.assertEqual(len(upload_features), 0)

    def test_delete_upload_application_feature_non_exist(self):
        response = self.client.delete(reverse('uploads_application_feature_api',
                                           kwargs={'pk': self.normalize_key(32),
                                                   'feature_id': self.normalize_key(233)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 204)
