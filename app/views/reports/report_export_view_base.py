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
from app.models.person import Person
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

    @staticmethod
    def get_date_string(date):
        if date:
            try:
                return date.strftime("%m/%d/%Y")
            except:
                return ''
        else:
            return ''
