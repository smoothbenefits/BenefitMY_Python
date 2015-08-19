from rest_framework.views import APIView
from rest_framework.response import Response

from django.http import HttpResponse
from django.http import Http404
from django.db import transaction
from django.db.models import Count, Max
from django.contrib.auth import get_user_model

from reportlab.pdfgen import canvas

from app.models.company_user import CompanyUser
from app.models.company import Company
from app.models.sys_period_definition import SysPeriodDefinition
from app.models.person import Person, SELF, SPOUSE, LIFE_PARTNER
from app.models.phone import Phone
from app.models.address import Address
from app.models.direct_deposit import DirectDeposit
from app.models.employee_profile import EmployeeProfile

from app.views.permission import (
    user_passes_test,
    company_employer,
    company_employer_or_broker)

class ReportExportViewBase(APIView):

    _user_employee_profile_dictionary = {}

    def _get_employee_profile_by_user_id(self, user_id):
        if user_id not in self._user_employee_profile_dictionary:
            try:
                person = Person.objects.filter(user=user_id, relationship='self')
                profiles = EmployeeProfile.objects.filter(person=person)
                if profiles:
                    self._user_employee_profile_dictionary[user_id] = profiles[0]
                else:
                    self._user_employee_profile_dictionary[user_id] = None;
            except Person.DoesNotExist:
                return None;
        return self._user_employee_profile_dictionary[user_id]


    def _get_max_dependents_count(self, company_id):
        users_id = self._get_all_employee_user_ids_for_company(company_id)
        persons = Person.objects.filter(user__in=users_id).exclude(relationship='self').exclude(relationship='spouse')

        # persons.groupby('user').count('pk').max()
        max_dependents = persons.values('user').annotate(num_dependents=Count('pk')).aggregate(max=Max('num_dependents'))

        result = max_dependents['max']

        if (result):
            return result

        return 0

    def _get_max_direct_deposit_count(self, company_id):
        user_ids = self._get_all_employee_user_ids_for_company(company_id)
        direct_deposits = DirectDeposit.objects.filter(user__in=user_ids)
        max_direct_deposits = direct_deposits.values('user').annotate(num_direct_deposit=Count('pk')).aggregate(max=Max('num_direct_deposit'))

        result = max_direct_deposits['max']
        if (result):
            return result
        return 0

    def _get_all_employee_user_ids_for_company(self, company_id):
        # Get all employees for the company
        users_id = []
        users = CompanyUser.objects.filter(company=company_id,
                                           company_user_type='employee')
        for user in users:
            users_id.append(user.user_id)

        return users_id

    def _get_company_by_user(self, user_id):
        company_model = None

        companies = CompanyUser.objects.filter(user=user_id)
        if (len(companies) > 0):
            company_model = companies[0].company

        return company_model

    def _get_person_basic_info_by_user(self, user_id):
        person_model = None

        persons = Person.objects.filter(user=user_id, relationship=SELF)
        if (len(persons) > 0):
            person_model = persons[0]

        return PersonInfo(person_model)

    def _get_person_basic_info(self, person_model):
        return PersonInfo(person_model)

    def _get_company_basic_info(self, company_model):
        return CompanyInfo(company_model)

    @staticmethod
    def get_date_string(date):
        if date:
            try:
                return date.strftime("%m/%d/%Y")
            except:
                return ''
        else:
            return ''

class PersonInfo(object):
    first_name = ''
    last_name = ''
    ssn = ''
    address1 = ''
    address2 = ''
    city = ''
    state = ''
    zipcode = ''
    country = 'USA'

    def __init__(self, person_model):
        if (person_model):
            self.first_name = person_model.first_name
            self.last_name = person_model.last_name
            self.ssn = person_model.ssn

            addresses = person_model.addresses.filter(address_type='home')
            if (len(addresses) > 0):
                address = addresses[0]
                self.address1 = address.street_1
                self.address2 = address.street_2
                self.city = address.city
                self.state = address.state
                self.zipcode = address.zipcode

    def get_full_name(self):
        if self.first_name is not None and self.last_name is not None:
            return self.first_name + ' ' + self.last_name
        return None

    def get_full_street_address(self):
        full_address = None
        if (self.address1 is not None):
            full_address = self.address1
            if (self.address2 is not None):
                full_address = full_address + ', ' + self.address2
        return full_address

    def get_country_and_zipcode(self):
        result = None
        if (self.country is not None):
            result = self.country
            if (self.zipcode is not None):
                result = result + ' ' + self.zipcode
        return result

class CompanyInfo(object):
    company_name = ''
    ein = ''
    address1 = ''
    address2 = ''
    city = ''
    state = ''
    zipcode = ''
    contact_phone = ''
    country = 'USA'
    offer_of_coverage_code = ''

    def __init__(self, company_model):
        if (company_model):
            self.company_name = company_model.name
            self.ein = company_model.ein
            self.offer_of_coverage_code = company_model.offer_of_coverage_code

            addresses = company_model.addresses.filter(address_type='main')
            if (len(addresses) > 0):
                address = addresses[0]
                self.address1 = address.street_1
                self.address2 = address.street_2
                self.city = address.city
                self.state = address.state
                self.zipcode = address.zipcode

            contacts = company_model.contacts.all()
            if (len(contacts) > 0):
                contact = contacts[0]
                phones = contact.phones.filter(phone_type='work')
                if (len(phones) > 0):
                    self.contact_phone = phones[0].number

    def get_full_street_address(self):
        full_address = None
        if (self.address1 is not None):
            full_address = self.address1
            if (self.address2 is not None):
                full_address = full_address + ', ' + self.address2
        return full_address

    def get_country_and_zipcode(self):
        result = None
        if (self.country is not None):
            result = self.country
            if (self.zipcode is not None):
                result = result + ' ' + self.zipcode
        return result