import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from app.views.tests.view_test_base import ViewTestBase

class CompanyGroupCompanySupplementalLifeInsuranceTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['23_auth_user',
                '49_period_definition', '10_company',
                '34_company_user',
                '61_company_group',
                '26_supplemental_life_insurance',
                '39_company_supplement_life_insurance',
                '64_company_group_supplemental_life_insurance_plan']

    def test_get_company_group_suppl_plan_by_company_group_success(self):
        response = self.client.get(reverse('company_group_supplemental_life_insurance_plan_api',
                                           kwargs={'company_group_id':self.normalize_key(2)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        array = json.loads(response.content)
        self.assertEqual(type(array), list)
        self.assertEqual(len(array), 1)
        result = array[0]
        self.assertEqual(type(result), dict)
        self.assertEqual(result['id'], self.normalize_key(1))
        self.assertEqual(result['company_suppl_life_insurance_plan']['id'], self.normalize_key(1))
        self.assertEqual(result['company_group']['id'], self.normalize_key(2))
        self.assertEqual(result['created_at'], '2015-04-24T16:16:02.760Z')
        self.assertEqual(result['updated_at'], '2015-04-24T16:16:02.760Z')

    def test_get_company_group_suppl_plan_by_company_group_empty(self):
        response = self.client.get(reverse('company_group_supplemental_life_insurance_plan_api',
                                           kwargs={'company_group_id':self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        array = json.loads(response.content)
        self.assertEqual(type(array), list)
        self.assertEqual(len(array), 0)

    def test_get_company_group_suppl_plan_by_company_group_non_exist(self):
        response = self.client.get(reverse('company_group_supplemental_life_insurance_plan_api',
                                           kwargs={'company_group_id':self.normalize_key(12)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        array = json.loads(response.content)
        self.assertEqual(type(array), list)
        self.assertEqual(len(array), 0)

    def test_get_company_group_suppl_plan_by_company_plan_success(self):
        response = self.client.get(reverse('company_group_supplemental_life_insurance_plan_by_company_plan_api',
                                           kwargs={'pk':self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        array = json.loads(response.content)
        self.assertEqual(type(array), list)
        self.assertEqual(len(array), 1)
        result = array[0]
        self.assertEqual(type(result), dict)
        self.assertEqual(result['id'], self.normalize_key(1))
        self.assertEqual(result['company_suppl_life_insurance_plan']['id'], self.normalize_key(1))
        self.assertEqual(result['company_group']['id'], self.normalize_key(2))
        self.assertEqual(result['created_at'], '2015-04-24T16:16:02.760Z')
        self.assertEqual(result['updated_at'], '2015-04-24T16:16:02.760Z')

    def test_get_company_group_suppl_plan_by_company_plan_empty(self):
        response = self.client.get(reverse('company_group_supplemental_life_insurance_plan_by_company_plan_api',
                                           kwargs={'pk':self.normalize_key(2)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        array = json.loads(response.content)
        self.assertEqual(type(array), list)
        self.assertEqual(len(array), 0)

    def test_get_company_group_suppl_plan_by_company_plan_non_exist(self):
        response = self.client.get(reverse('company_group_supplemental_life_insurance_plan_by_company_plan_api',
                                           kwargs={'pk':self.normalize_key(12)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)


    def test_put_company_group_suppl_plan_by_company_plan_success(self):
        company_group_data = [
                                {'company_group': self.normalize_key(3),
                                 'company_suppl_life_insurance_plan': self.normalize_key(1)
                                },
                                {'company_group': self.normalize_key(1),
                                 'company_suppl_life_insurance_plan': self.normalize_key(1)
                                }
                             ]
        response = self.client.put(reverse('company_group_supplemental_life_insurance_plan_by_company_plan_api',
                                           kwargs={'pk':self.normalize_key(1)}),
                                   data=json.dumps(company_group_data),
                                   content_type='application/json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)

        response = self.client.get(reverse('company_group_supplemental_life_insurance_plan_by_company_plan_api',
                                           kwargs={'pk':self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        array = json.loads(response.content)
        self.assertEqual(type(array), list)
        self.assertEqual(len(array), 2)

        array = sorted(array, key=lambda x: x['id'])

        result = array[0]
        self.assertEqual(type(result), dict)
        self.assertEqual(result['id'], self.normalize_key(2))
        self.assertEqual(result['company_suppl_life_insurance_plan']['id'], self.normalize_key(1))
        self.assertEqual(result['company_group']['id'], self.normalize_key(3))
        result = array[1]
        self.assertEqual(type(result), dict)
        self.assertEqual(result['id'], self.normalize_key(3))
        self.assertEqual(result['company_suppl_life_insurance_plan']['id'], self.normalize_key(1))
        self.assertEqual(result['company_group']['id'], self.normalize_key(1))

    def test_put_company_group_suppl_plan_by_company_plan_non_exist(self):
        company_group_data = [
                                {'company_group': self.normalize_key(3),
                                 'company_suppl_life_insurance_plan': self.normalize_key(1)
                                },
                                {'company_group': self.normalize_key(1),
                                 'company_suppl_life_insurance_plan': self.normalize_key(1)
                                }
                             ]
        response = self.client.put(reverse('company_group_supplemental_life_insurance_plan_by_company_plan_api',
                                           kwargs={'pk':self.normalize_key(12)}),
                                   data=json.dumps(company_group_data),
                                   content_type='application/json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)

    def test_post_company_group_suppl_plan_by_company_plan_success(self):
        company_group_data = [
                                {'company_group': self.normalize_key(1),
                                 'company_suppl_life_insurance_plan': self.normalize_key(2)
                                },
                                {'company_group': self.normalize_key(2),
                                 'company_suppl_life_insurance_plan': self.normalize_key(2)
                                }
                             ]
        response = self.client.post(reverse('company_group_supplemental_life_insurance_plan_by_company_plan_api',
                                            kwargs={'pk':self.normalize_key(2)}),
                                    data=json.dumps(company_group_data),
                                    content_type='application/json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)

        response = self.client.get(reverse('company_group_supplemental_life_insurance_plan_by_company_plan_api',
                                           kwargs={'pk':self.normalize_key(2)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        array = json.loads(response.content)
        self.assertEqual(type(array), list)
        self.assertEqual(len(array), 2)

        array = sorted(array, key=lambda x: x['id'])

        result = array[0]
        self.assertEqual(type(result), dict)
        self.assertEqual(result['id'], self.normalize_key(2))
        self.assertEqual(result['company_suppl_life_insurance_plan']['id'], self.normalize_key(2))
        self.assertEqual(result['company_group']['id'], self.normalize_key(1))
        result = array[1]
        self.assertEqual(type(result), dict)
        self.assertEqual(result['id'], self.normalize_key(3))
        self.assertEqual(result['company_suppl_life_insurance_plan']['id'], self.normalize_key(2))
        self.assertEqual(result['company_group']['id'], self.normalize_key(2))

    def test_post_company_group_suppl_plan_by_company_plan_non_exist(self):
        company_group_data = [
                                {'company_group': self.normalize_key(3),
                                 'company_suppl_life_insurance_plan': self.normalize_key(1)
                                },
                                {'company_group': self.normalize_key(1),
                                 'company_suppl_life_insurance_plan': self.normalize_key(1)
                                }
                             ]
        response = self.client.post(reverse('company_group_supplemental_life_insurance_plan_by_company_plan_api',
                                            kwargs={'pk':self.normalize_key(12)}),
                                    data=json.dumps(company_group_data),
                                    content_type='application/json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)

    def test_delete_company_group_suppl_plan_by_company_plan_success(self):
        response = self.client.delete(reverse('company_group_supplemental_life_insurance_plan_by_company_plan_api',
                                            kwargs={'pk':self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, '')

        response = self.client.get(reverse('company_group_supplemental_life_insurance_plan_by_company_plan_api',
                                           kwargs={'pk':self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        array = json.loads(response.content)
        self.assertEqual(type(array), list)
        self.assertEqual(len(array), 0)

    def test_delete_company_group_suppl_plan_by_company_plan_non_exist(self):
        response = self.client.delete(reverse('company_group_supplemental_life_insurance_plan_by_company_plan_api',
                                            kwargs={'pk':self.normalize_key(14)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, '')

        response = self.client.get(reverse('company_group_supplemental_life_insurance_plan_by_company_plan_api',
                                           kwargs={'pk':self.normalize_key(14)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)
