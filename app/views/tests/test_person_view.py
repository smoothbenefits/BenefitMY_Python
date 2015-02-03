import json
from django.test import TestCase
from django.core.urlresolvers import reverse
import json


class PersonTestCase(TestCase):
    # your fixture files here
    fixtures = ['24_person', '10_company', '23_auth_user', '11_address',
                '12_phone']

    def test_get_person_existing(self):
        response = self.client.get(reverse('people_by_id', kwargs={'pk': 1}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.content, '')
        person_response = json.loads(response.content)
        self.assertIn('person', person_response)
        person = person_response['person']
        self.assertTrue('id' in person and person['id']==1)
        self.assertTrue('person_type' in person and person['person_type']=='primary_contact')
        self.assertTrue('relationship' in person and person['relationship']=='self')
        self.assertTrue('first_name' in person and person['first_name']=='John')
        self.assertTrue('last_name' in person and person['last_name']=='Hancock')
        self.assertTrue('email' in person and not person['email'])
        self.assertNotIn('ssn', person)
        self.assertTrue('birth_date' in person and person['birth_date']=='1978-09-05')
        self.assertTrue('user' in person and person['user']==1)
        self.assertTrue('company' in person and person['company']==1)
        self.assertIn('emergency_contact', person)
        person_emergency_contact = person['emergency_contact']
        self.assertEqual(len(person_emergency_contact), 0) 

    def test_get_person_non_exist(self):
        response=self.client.get(reverse('people_by_id', kwargs={'pk':444}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)
        not_found_response = json.loads(response.content)
        self.assertTrue('detail' in not_found_response and not_found_response['detail']=='Not found')

    def test_get_person_another_existing(self):
        response = self.client.get(reverse('people_by_id', kwargs={'pk': 4}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.content, '')
        person_response = json.loads(response.content)
        self.assertIn('person', person_response)
        person = person_response['person']
        self.assertTrue('id' in person and person['id']==4)
        self.assertTrue('person_type' in person and person['person_type']=='family')
        self.assertTrue('relationship' in person and person['relationship']=='spouse')
        self.assertTrue('first_name' in person and person['first_name']=='Christina')
        self.assertTrue('last_name' in person and person['last_name']=='Cowell')
        self.assertTrue('email' in person and person['email'] == 'christina.cowell@hotmail.com')
        self.assertNotIn('ssn', person)
        self.assertTrue('birth_date' in person and person['birth_date']=='1983-01-02')
        self.assertTrue('user' in person and person['user']==3)
        self.assertTrue('company' in person and not person['company'])
        self.assertIn('emergency_contact', person)
        person_emergency_contact = person['emergency_contact']
        self.assertEqual(len(person_emergency_contact), 0) 
