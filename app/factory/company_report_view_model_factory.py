from app.models.company_user import CompanyUser
from app.models.person import Person, SELF
from app.models.company import Company
from app.models.employee_profile import (
    EmployeeProfile,
    FULL_TIME
)
from app.models.aca.employee_1095_c import Employee1095C
from app.models.aca.company_1095_c import Company1095C, PERIODS
from app.models.aca.company_1094_c_member_info import Company1094CMemberInfo
from app.models.aca.company_1094_c_monthly_member_info import Company1094CMonthlyMemberInfo
from app.models.employment_authorization import EmploymentAuthorization
from app.models.w4 import W4
from app.models.tax.employee_state_tax_election import EmployeeStateTaxElection

from app.view_models.person_info import PersonInfo
from app.view_models.company_info import CompanyInfo
from app.view_models.employee_employment_profile_info import EmployeeEmploymentProfileInfo
from app.view_models.report.employee_1095_c_data import Employee1095CData
from app.view_models.report.company_1094_c_data import Company1094CData
from app.view_models.report.employee_i9_data import EmployeeI9Data
from app.view_models.report.employee_w4_data import EmployeeW4Data
from app.view_models.employee_state_tax_info import EmployeeStateTaxInfo
from django.http import Http404


''' This factory will attempt at eager loading all appropriate data about
    the given company, as a potential way to accelerate the data collection
    within. This is appropriate to use in the case where the factory is 
    expected to be invoked over and over again on list of employees from the 
    company
'''
class CompanyReportViewModelFactory(object):
    def __init__(self, company_id):
        self._company_employee_user_ids = self._get_all_employee_user_ids_for_company(company_id)

        self._company_model = Company.objects.get(pk=company_id)

        person_models = Person.objects.filter(user__in=self._company_employee_user_ids, relationship=SELF)
        self._company_employee_persons = {p.user.id: p for p in person_models} 

        i9_models = EmploymentAuthorization.objects.filter(user__in=self._company_employee_user_ids)
        self._company_i9s = {ea.user.id: ea for ea in i9_models}

        w4_models = W4.objects.filter(user__in=self._company_employee_user_ids)
        self._company_w4s = {w4.user.id: w4 for w4 in w4_models}

        self._state_tax_models = EmployeeStateTaxElection.objects.filter(user__in=self._company_employee_user_ids)

        employee_profile_models = EmployeeProfile.objects.filter(company=company_id)
        self._company_employee_profiles = {profile.person.user.id: profile for profile in employee_profile_models}

    def get_employee_person_info(self, employee_user_id):
        return PersonInfo(self._company_employee_persons.get(employee_user_id))

    def get_company_info(self):
        return CompanyInfo(self._company_model)

    def get_employee_i9_data(self, user_id):
        i9_model = self._company_i9s.get(user_id)
        if (not i9_model):
            return None
        return EmployeeI9Data(i9_model)

    def get_employee_w4_data(self, user_id):
        w4_model = self._company_w4s.get(user_id)
        if (not w4_model):
            return None
        return EmployeeW4Data(w4_model)

    def get_employee_state_tax_data(self, user_id):
        election_models = [election for election in self._state_tax_models if election.user.id == user_id]
        return EmployeeStateTaxInfo(election_models)

    def get_employee_employment_profile_data(self, employee_user_id, company_id):
        person_model = self._company_employee_persons.get(employee_user_id)

        if (not person_model): 
            return None

        profile_model = self._company_employee_profiles.get(employee_user_id)

        return EmployeeEmploymentProfileInfo(person_model, company_id, employee_user_id, profile_model)

    def _get_person_by_user(self, user_id):
        person_model = None

        persons = Person.objects.filter(user=user_id, relationship=SELF)
        if (len(persons) > 0):
            person_model = persons[0]

        return person_model

    def _get_all_employee_user_ids_for_company(self, company_id):
        # Get all employees for the company
        users = []
        comp_users = CompanyUser.objects.filter(company=company_id,
                                           company_user_type='employee')
        for comp_user in comp_users:
            if (comp_user.user):
                users.append(comp_user.user.id)

        return users
