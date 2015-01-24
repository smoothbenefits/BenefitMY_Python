from django.test import TestCase
import django
django.test.utils.setup_test_environment()

PREFIX = "api/v1"


class PersonTestCase(TestCase):
    # your fixture files here
    fixtures = ['app/fixtures/people.json', 'company.json', 'user.json']


    def test_get_person(self):
        response = self.client.get('api/v1/person/1')
        print "response", response
        print "content", response.content
        print "context", response.context
        print "client", response.client
        #self.assertEqual(response.status_code, 200)
        #self.assertEqual(response.content, "")
