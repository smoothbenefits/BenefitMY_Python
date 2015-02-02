from django.test import TestCase
from django.core.urlresolvers import reverse
import json


class DocumentTypeTestCase(TestCase):
    # your fixture files here
    fixtures = ['14_document_type']

    def test_get_document_type(self):
        response = self.client.get(reverse('document_type_api'))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result['document_types']), list)
        self.assertEqual(result['document_types'][0]['id'], 1)
        self.assertEqual(result['document_types'][0]['name'], 'Offer Letter')

        self.assertEqual(result['document_types'][2]['id'], 3)
        self.assertEqual(result['document_types'][2]['name'], 'NDA')
