from django.test import TestCase
from django.core.urlresolvers import reverse
import json


class PersonTestCase(TestCase):
    # your fixture files here
    fixtures = ['24_person', '10_company', '23_auth_user', '11_address',
                '12_phone']

    def test_get_person(self):
        response = self.client.get(reverse('people_api',
                                           kwargs={'pk': 1}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(result['person']['first_name'], 'John')
        self.assertEqual(result['person']['last_name'], 'Hancock')
        self.assertEqual(result['person']['addresses'][0]['zipcode'],
                         '02141')
        self.assertEqual(result['person']['phones'][0]['number'],
                         '6078980780')

    def test_del_person(self):
        response = self.client.delete(reverse('people_api',
                                              kwargs={'pk': 1}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(result['deleted_person']['first_name'], 'John')
        self.assertEqual(result['deleted_person']['last_name'], 'Hancock')
