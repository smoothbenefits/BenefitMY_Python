import json
import sys
import copy
from django.test import TestCase
from django.core.urlresolvers import reverse
from view_test_base import ViewTestBase


class PersonTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['24_person', 
                '10_company', 
                '23_auth_user', 
                '11_address',
                '12_phone']

    def setUp(self):
        self.new_person = {
            'person_type':'family',
            'first_name': 'test_create',
            'last_name': 'tested',
            'email': 'tester@mail.com',
            'relationship':'dependent',
            'ssn': '233-432-5444',
            'birth_date':'1982-09-02',
            'gender':'M',
            'user': self.normalize_key(3),
            'addresses':[{'address_type':'primary',
                          'street_1': '3243 Mass ave',
                          'street_2':'',
                          'city': 'Waltham',
                          'state': 'MA',
                          'zipcode': '03233'}],
            'phones':[{'phone_type':'home',
                       'number': '972-343-9938'}],
            'emergency_contact':[]
        }

    def test_get_person_existing(self):
        response = self.client.get(reverse('people_by_id', kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.content, '')
        person_response = json.loads(response.content)
        self.assertIn('person', person_response)
        person = person_response['person']
        self.assertTrue('id' in person and person['id']==self.normalize_key(1))
        self.assertTrue('person_type' in person and person['person_type']=='primary_contact')
        self.assertTrue('relationship' in person and person['relationship']=='self')
        self.assertTrue('first_name' in person and person['first_name']=='John')
        self.assertTrue('last_name' in person and person['last_name']=='Hancock')
        self.assertTrue('email' in person and not person['email'])
        self.assertTrue('gender' in person and person['gender']=='F')
        self.assertNotIn('ssn', person)
        self.assertTrue('birth_date' in person and person['birth_date']=='1978-09-05')
        self.assertTrue('user' in person and person['user']==self.normalize_key(1))
        self.assertTrue('company' in person and person['company']==self.normalize_key(1))
        self.assertIn('emergency_contact', person)
        person_emergency_contact = person['emergency_contact']
        self.assertEqual(len(person_emergency_contact), 0)

    def test_get_person_non_exist(self):
        response=self.client.get(reverse('people_by_id', kwargs={'pk':self.normalize_key(444)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)
        not_found_response = json.loads(response.content)
        self.assertTrue('detail' in not_found_response and not_found_response['detail']=='Not found')

    def test_get_person_another_existing(self):
        response = self.client.get(reverse('people_by_id', kwargs={'pk': self.normalize_key(4)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.content, '')
        person_response = json.loads(response.content)
        self.assertIn('person', person_response)
        person = person_response['person']
        self.assertTrue('id' in person and person['id']==self.normalize_key(4))
        self.assertTrue('person_type' in person and person['person_type']=='family')
        self.assertTrue('relationship' in person and person['relationship']=='spouse')
        self.assertTrue('first_name' in person and person['first_name']=='Christina')
        self.assertTrue('last_name' in person and person['last_name']=='Cowell')
        self.assertTrue('email' in person and person['email'] == 'christina.cowell@hotmail.com')
        self.assertNotIn('ssn', person)
        self.assertTrue('birth_date' in person and person['birth_date']=='1983-01-02')
        self.assertTrue('user' in person and person['user']==self.normalize_key(3))
        self.assertTrue('company' in person and not person['company'])
        self.assertIn('emergency_contact', person)
        person_emergency_contact = person['emergency_contact']
        self.assertEqual(len(person_emergency_contact), 0)


    def test_get_user_family(self):
        response = self.client.get(reverse('user_family_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(type(result['family']), list)
        self.assertEqual(result['first_name'], 'John')
        self.assertEqual(result['last_name'], 'Hancock')
        self.assertEqual(result['id'], self.normalize_key(1))
        self.assertEqual(result['email'], 'user1@benefitmy.com')
        self.assertEqual(result['family'][0]['id'], self.normalize_key(1))
        self.assertEqual(result['family'][0]['relationship'], 'self')
        self.assertEqual(result['family'][0]['birth_date'], '1978-09-05')

        response = self.client.get(reverse('user_family_api',
                                           kwargs={'pk': self.normalize_key(3)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(type(result['family']), list)
        self.assertEqual(result['first_name'], 'Simon')
        self.assertEqual(result['last_name'], 'Cowell')
        self.assertEqual(result['id'], self.normalize_key(3))
        self.assertEqual(result['email'], 'user3@benefitmy.com')
        family = sorted(result['family'], key=lambda member: member['id'])
        self.assertEqual(family[0]['id'], self.normalize_key(3))
        self.assertEqual(family[0]['relationship'], 'self')
        self.assertEqual(family[0]['birth_date'], '1988-05-27')
        self.assertEqual(family[1]['id'], self.normalize_key(4))
        self.assertEqual(family[1]['relationship'], 'spouse')
        self.assertEqual(family[1]['birth_date'], '1983-01-02')

    def test_get_family_by_non_exist_user(self):
        response=self.client.get(reverse('user_family_api', kwargs={'pk':self.normalize_key(sys.maxint)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)

    def test_get_family_by_exist_user_non_exist_person(self):
        response=self.client.get(reverse('user_family_api', kwargs={'pk':self.normalize_key(4)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertIn('family', result)
        self.assertEqual(len(result['family']), 0)

    def test_create_new_family_member_success(self):
        response = self.client.post(reverse('user_family_api', kwargs={'pk':self.normalize_key(3)}), 
                                    data=json.dumps(self.new_person),
                                    content_type='application/json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.content)
        self.assertIn('id', result)

    def test_create_new_family_member_repeat_spouse(self):
        another=copy.deepcopy(self.new_person)
        another['relationship'] = 'spouse'
        response = self.client.post(reverse('user_family_api', kwargs={'pk':self.normalize_key(3)}), 
                                    data=json.dumps(another),
                                    content_type='application/json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.content)
        self.assertIn('message', result)
        self.assertEqual(result['message'], 'Cannot add a new spouse when you already have a spouse in DB')
