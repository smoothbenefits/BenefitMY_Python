from django.db.models import Prefetch
from app.models.company_user import CompanyUser
from app.models.person import Person, SELF
from app.models.company import Company
from app.models.employee_profile import (
    EmployeeProfile,
    FULL_TIME
)
from app.models.employee_compensation import EmployeeCompensation
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


''' This factory will attempt at eager loading all appropriate data about
    the given company, as a potential way to accelerate the data collection
    within. This is appropriate to use in the case where the factory is 
    expected to be invoked over and over again on list of employees from the 
    company
'''
class CompanyReportViewModelFactory(object):
    def __init__(self, company_id):
        self._company_employee_user_ids = self._get_all_employee_user_ids_for_company(company_id)

        # I honest don't like the deep optimization of indirect relationships
        # such as the person-to-compensation links. This whole thing is by
        # nature by convention, and this would not produce manageable code.
        # Though I did my best to try to at least keep the downstream code 
        # (e.g. in this case, CompensationService, PersonInfo, etc.) relatively
        # agnostic about this. i.e. they should function with or without these 
        # optimization. 
        # But certain things, such as the "all_compensations_ordered_by_effective_date"
        # attribute attached to the person model object below, is simply forced on
        # me, and requires human documentation and memory. Not so bad, just ugly...
        # Hence, I deliberately made the name long and specific, so it is at least
        # very easy to pin down where this freaking attribute is defined. 
        person_models = Person.objects \
            .select_related('user') \
            .prefetch_related('addresses') \
            .prefetch_related('phones') \
            .prefetch_related(
                Prefetch(
                    'employee_compensation_person',
                    to_attr='all_compensations_ordered_by_effective_date',
                    queryset=EmployeeCompensation.objects.select_related('reason').order_by('effective_date', 'id'))
            ) \
            .filter(user__in=self._company_employee_user_ids, relationship=SELF)
        self._company_employee_persons = {p.user.id: p for p in person_models} 

        self._company_model = Company.objects \
            .select_related('pay_period_definition') \
            .get(pk=company_id)
        self._company_info = CompanyInfo(self._company_model)

        i9_models = EmploymentAuthorization.objects.select_related().filter(user__in=self._company_employee_user_ids)
        self._company_i9s = {ea.user.id: ea for ea in i9_models}

        w4_models = W4.objects.select_related().filter(user__in=self._company_employee_user_ids)
        self._company_w4s = {w4.user.id: w4 for w4 in w4_models}

        self._state_tax_models = list(EmployeeStateTaxElection.objects.select_related().filter(user__in=self._company_employee_user_ids))

        employee_profile_models = EmployeeProfile.objects \
            .select_related('employee_profile_pay_rate') \
            .select_related('person') \
            .select_related('person__user') \
            .select_related('company') \
            .select_related('department') \
            .select_related('job') \
            .select_related('division') \
            .select_related('manager') \
            .filter(company=company_id)
        self._company_employee_profiles = {profile.person.user.id: profile for profile in employee_profile_models}

    def get_employee_person_info(self, employee_user_id):
        person_info = PersonInfo(self._company_employee_persons.get(employee_user_id))
        return person_info

    def get_company_info(self):
        return self._company_info

    def get_employee_i9_data(self, user_id):
        i9_model = self._company_i9s.get(user_id)
        if (not i9_model):
            return None
        i9_info = EmployeeI9Data(i9_model)
        return i9_info

    def get_employee_w4_data(self, user_id):
        w4_model = self._company_w4s.get(user_id)
        if (not w4_model):
            return None
        w4_info = EmployeeW4Data(w4_model)
        return w4_info

    def get_employee_state_tax_data(self, user_id):
        election_models = [election for election in self._state_tax_models if election.user.id == user_id]
        state_tax_info = EmployeeStateTaxInfo(election_models)
        return state_tax_info

    def get_employee_employment_profile_data(self, employee_user_id):
        person_model = self._company_employee_persons.get(employee_user_id)

        if (not person_model): 
            return None

        profile_model = self._company_employee_profiles.get(employee_user_id)

        profile_info = EmployeeEmploymentProfileInfo(person_model, self._company_model, employee_user_id, profile_model)
        return profile_info

    def _get_all_employee_user_ids_for_company(self, company_id):
        # Get all employees for the company
        users = []
        comp_users = CompanyUser.objects \
            .select_related('user') \
            .select_related('company') \
            .filter(company=company_id, company_user_type='employee')
        for comp_user in comp_users:
            if (comp_user.user):
                users.append(comp_user.user.id)

        return users
