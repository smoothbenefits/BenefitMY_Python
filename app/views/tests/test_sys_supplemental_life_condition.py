import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from view_test_base import ViewTestBase

class SysSupplementalLifeConditionTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['17_supplemental_life_insurance_condition']

    def test_get_supplemental_life_insurance_condition(self):
        data = [(1, 'Unknown'), (2, 'Tobacco'), (3, 'Non-Tobacco'), (4, 'Other')]

        response = self.client.get(reverse('suppl_life_condition'))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 4)

        for datum in data:
            entry = next(r for r in result if r['id'] == self.normalize_key(datum[0]))
            self.assertEqual(entry['name'], datum[1])
