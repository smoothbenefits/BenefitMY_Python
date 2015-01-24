from django.test import TestCase
import django
from django.core.urlresolvers import reverse


PREFIX = "api/v1"


class PersonTestCase(TestCase):
    # your fixture files here
    fixtures = ['people', 'company', 'user']


    def test_get_person(self):
        response = self.client.get(reverse('people_api', kwargs={'pk': 1}))
        print "response", response
        print "content", response.content
        print "context", response.context
        print "client", response.client
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        