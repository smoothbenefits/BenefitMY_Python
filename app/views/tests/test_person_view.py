from django.test import TestCase
from django.core.urlresolvers import reverse


class PersonTestCase(TestCase):
    # your fixture files here
    fixtures = ['24_person', '10_company', '23_auth_user', '11_address',
                '12_phone']

    def test_get_person(self):
        response = self.client.get(reverse('people_api', kwargs={'pk': 1}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
