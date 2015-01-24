from django.test import TestCase
from django.core.urlresolvers import reverse

class PersonTestCase(TestCase):
    # your fixture files here
    fixtures = ['people', 'company', 'user']


    def test_get_person(self):
        response = self.client.get(reverse('people_api', kwargs={'pk': 1}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        