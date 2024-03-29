import json
from django.conf import settings
from django.test import TestCase
from django.core.urlresolvers import reverse
from view_test_base import ViewTestBase


class UploadTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['23_auth_user', 'upload', '49_period_definition', '10_company', '34_company_user']

    def setUp(self):
        self.upload_data = {
            'company': self.normalize_key(1),
            'user': self.normalize_key(3),
            'file_name': 'tester.pdf',
            'file_type': 'application/pdf',
            'company_name': 'carbonite',
        }

    def test_get_uploads_by_user_success(self):
        response = self.client.get(reverse('uploads_by_user',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 2)
        upload1 = None
        for x in result:
            if x['id'] == self.normalize_key(7):
                upload1 = x
                break
        self.assertEqual(upload1['S3'], 'https://benefitmy-demo-uploads.s3.amazonaws.com/BenefitMy_Inc.:MV9fMV9fMjAxNS0wNS0wNiAwMDowODoyNC43MjQxNDM=:55-0925_2015_HMO_NE_SG_Product_Chart.pdf')
        self.assertEqual(upload1['file_type'], 'application/pdf')
        self.assertEqual(upload1['file_name'], '55-0925_2015_HMO_NE_SG_Product_Chart.pdf')
        self.assertEqual(upload1['company'], self.normalize_key(1))
        self.assertEqual(upload1['user'], self.normalize_key(1))
        self.assertEqual(upload1['id'], self.normalize_key(7))
        upload2 = None
        for x in result:
            if x['id'] == self.normalize_key(8):
                upload2 = x
                break
        self.assertEqual(upload2['S3'], 'https://benefitmy-demo-uploads.s3.amazonaws.com/BenefitMy_Inc.:MV9fMV9fMjAxNS0wNS0wNiAwMDowODo1NC42ODQ5NDA=:55-0924_2015_PPO_SG_Product_Chart.pdf')
        self.assertEqual(upload2['file_type'], 'application/pdf')
        self.assertEqual(upload2['file_name'], '55-0924_2015_PPO_SG_Product_Chart.pdf')
        self.assertEqual(upload2['company'], self.normalize_key(1))
        self.assertEqual(upload2['user'], self.normalize_key(1))
        self.assertEqual(upload2['id'], self.normalize_key(8))

    def test_get_uploads_by_user_empty(self):
        response = self.client.get(reverse('uploads_by_user',
                                           kwargs={'pk': self.normalize_key(5)}))
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
                                           kwargs={'pk': self.normalize_key(3)}),
                                    data=json.dumps(self.upload_data),
                                    content_type='application/json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.content)
        self.assertTrue('S3' in result)
        self.assertIsNotNone(result['S3'])
        self.assertEqual(result['file_type'], self.upload_data['file_type'])
        self.assertEqual(result['file_name'], self.upload_data['file_name'])
        self.assertEqual(result['company'], 1)
        self.assertEqual(result['user'], 3)
        self.assertEqual(result['id'], self.normalize_key(10))
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
                                           kwargs={'pk': self.normalize_key(3)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 2)
        upload1 = None
        for x in result:
            if x['id'] == self.normalize_key(9):
                upload1 = x
                break
        self.assertEqual(upload1['file_type'], 'image/jpeg')
        self.assertEqual(upload1['file_name'], 'MA Dirver License.jpg')
        self.assertEqual(upload1['company'], self.normalize_key(1))
        self.assertEqual(upload1['user'], self.normalize_key(3))
        self.assertEqual(upload1['id'], self.normalize_key(9))
        upload2 = None
        for x in result:
            if x['id'] == self.normalize_key(10):
                upload2 = x
                break
        self.assertIsNotNone(upload2['S3'], 'https://benefitmy-demo-uploads.s3.amazonaws.com/BenefitMy_Inc.:MV9fM19fMjAxNS0wNS0wNiAwMDoyMzozMi45MzAyODk=:MA_Dirver_License.jpg')
        self.assertEqual(upload2['file_type'], self.upload_data['file_type'])
        self.assertEqual(upload2['file_name'], self.upload_data['file_name'])
        self.assertEqual(upload2['company'], self.normalize_key(1))
        self.assertEqual(upload2['user'], self.normalize_key(3))
        self.assertEqual(upload2['id'], self.normalize_key(10))

    def test_upload_post_with_non_exist_user(self):
        self.upload_data.update({'user': self.normalize_key(128)})
        response = self.client.post(reverse('uploads_by_user',
                                           kwargs={'pk': self.normalize_key(4)}),
                                    data=json.dumps(self.upload_data),
                                    content_type='application/json')

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)
        self.assertIsNotNone(response.content)


    def test_upload_post_with_non_exist_company(self):
        self.upload_data.update({'company': self.normalize_key(122)})
        response = self.client.post(reverse('uploads_by_user',
                                           kwargs={'pk': self.normalize_key(4)}),
                                    data=json.dumps(self.upload_data),
                                    content_type='application/json')

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)
        self.assertIsNotNone(response.content)

    def test_delete_upload_success(self):
        response = self.client.delete(reverse('upload_api',
                                           kwargs={'pk': self.normalize_key(3)}))
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
        self.assertEqual(upload1['S3'], 'https://benefitmy-demo-uploads.s3.amazonaws.com/BenefitMy_Inc.:MV9fM19fMjAxNS0wNS0wNiAwMDoyMzozMi45MzAyODk=:MA_Dirver_License.jpg')
        self.assertEqual(upload1['file_type'], 'image/jpeg')
        self.assertEqual(upload1['file_name'], 'MA Dirver License.jpg')
        self.assertEqual(upload1['company'], self.normalize_key(1))
        self.assertEqual(upload1['user'], self.normalize_key(3))
        self.assertEqual(upload1['id'], self.normalize_key(9))

    def test_delete_upload_non_exist(self):
        response = self.client.delete(reverse('upload_api',
                                           kwargs={'pk': self.normalize_key(78)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)
        self.assertIsNotNone(response.content)


    def test_get_by_id_success(self):
        response = self.client.get(reverse('upload_api',
                                           kwargs={'pk': self.normalize_key(5)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        upload1 = json.loads(response.content)
        self.assertEqual(upload1['S3'], 'https://benefitmy-dev-uploads.s3.amazonaws.com/Greencard.jpeg')
        self.assertEqual(upload1['file_type'], 'image/jpeg')
        self.assertEqual(upload1['file_name'], 'Greencard.jpeg')
        self.assertEqual(upload1['company'], self.normalize_key(1))
        self.assertEqual(upload1['user'], self.normalize_key(2))
        self.assertEqual(upload1['id'], self.normalize_key(5))

    def test_get_by_id_non_exist(self):
        response = self.client.get(reverse('upload_api',
                                           kwargs={'pk': self.normalize_key(90)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)
        self.assertIsNotNone(response.content)

    def test_get_uploads_by_employer_success(self):
        user_id = self.normalize_key(3)
        comp_id = self.normalize_key(1)
        # need to login
        login_resp = self.client.login(username='user2@benefitmy.com', password='foobar')
        self.assertTrue(login_resp)
        self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual(self.client.session['_auth_user_id'], 2)
        response = self.client.get(reverse('get_comp_uploads',
                                           kwargs={'comp_id': comp_id,
                                                   'pk': user_id}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        uploads = json.loads(response.content)
        self.assertEqual(len(uploads), 1)
        upload1 = None
        for x in uploads:
            if x['id'] == self.normalize_key(9):
                upload1 = x
                break
        self.assertEqual(upload1['S3'], 'https://benefitmy-demo-uploads.s3.amazonaws.com/BenefitMy_Inc.:MV9fM19fMjAxNS0wNS0wNiAwMDoyMzozMi45MzAyODk=:MA_Dirver_License.jpg')
        self.assertEqual(upload1['file_type'], 'image/jpeg')
        self.assertEqual(upload1['file_name'], 'MA Dirver License.jpg')
        self.assertEqual(upload1['company'], self.normalize_key(1))
        self.assertEqual(upload1['user'], self.normalize_key(3))
        self.assertEqual(upload1['id'], self.normalize_key(9))

    def test_get_uploads_by_employer_bad_current_user(self):
        user_id = self.normalize_key(3)
        comp_id = self.normalize_key(1)
        # need to login
        login_resp = self.client.login(username='user4@benefitmy.com', password='foobar')
        self.assertTrue(login_resp)
        self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual(self.client.session['_auth_user_id'], 4)
        response = self.client.get(reverse('get_comp_uploads',
                                           kwargs={'comp_id': comp_id,
                                                   'pk': user_id}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 405)
        uploads = json.loads(response.content)
        self.assertIn('message', uploads)
        self.assertIn('do not match', uploads['message'])

    def test_get_uploads_by_employer_bad_company(self):
        user_id = self.normalize_key(3)
        comp_id = self.normalize_key(44)
        # need to login
        login_resp = self.client.login(username='user2@benefitmy.com', password='foobar')
        self.assertTrue(login_resp)
        self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual(self.client.session['_auth_user_id'], 2)
        response = self.client.get(reverse('get_comp_uploads',
                                           kwargs={'comp_id': comp_id,
                                                   'pk': user_id}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 405)
        uploads = json.loads(response.content)
        self.assertIn('message', uploads)
        self.assertIn('do not match', uploads['message'])

    def test_get_uploads_by_employer_bad_employee(self):
        user_id = self.normalize_key(55)
        comp_id = self.normalize_key(1)
        # need to login
        login_resp = self.client.login(username='user2@benefitmy.com', password='foobar')
        self.assertTrue(login_resp)
        self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual(self.client.session['_auth_user_id'], 2)
        response = self.client.get(reverse('get_comp_uploads',
                                           kwargs={'comp_id': comp_id,
                                                   'pk': user_id}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 405)
        uploads = json.loads(response.content)
        self.assertIn('message', uploads)
        self.assertIn('do not match', uploads['message'])
