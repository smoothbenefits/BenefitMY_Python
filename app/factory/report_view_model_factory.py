from app.models.company_user import CompanyUser
from app.models.person import Person, SELF
from app.models.company import Company
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


class ReportViewModelFactory(object):
    def get_employee_person_info(self, employee_user_id):
        return PersonInfo(self._get_person_by_user(employee_user_id))

    def get_company_info(self, company_id):
        try:
            company_model = Company.objects.get(pk=company_id)
            return CompanyInfo(company_model)
        except Company.DoesNotExist:
            raise Http404

    def get_employee_company_info(self, employee_user_id):
        return CompanyInfo(self._get_company_by_user(employee_user_id))

    def get_employee_employment_profile_data(self, employee_user_id, company_id):
        person_model = self._get_person_by_user(employee_user_id)

        if (not person_model): 
            return None

        return EmployeeEmploymentProfileInfo(person_model, company_id, employee_user_id)

    def get_employee_1095_c_data(self, employee_user_id, company_id):
        return self._get_employee_1095_c_data_collection(employee_user_id, company_id)

    def get_company_1094_c_data(self, company_id):
        return self._get_company_1094_c_data(company_id)

    def get_employee_i9_data(self, user_id):
        return self._get_employee_i9_data(user_id)

    def get_employee_w4_data(self, user_id):
        return self._get_employee_w4_data(user_id)

    def get_employee_state_tax_data(self, user_id):
        return self._get_employee_state_tax_info(user_id)

    def _get_person_by_user(self, user_id):
        person_model = None

        persons = Person.objects.filter(user=user_id, relationship=SELF)
        if (len(persons) > 0):
            person_model = persons[0]

        return person_model

    def _get_company_by_user(self, user_id):
        company_model = None

        companies = CompanyUser.objects.filter(user=user_id)
        if (len(companies) > 0):
            company_model = companies[0].company

        return company_model

    def _get_employee_1095_c_data_collection(self, user_id, company_id):
        person = self._get_person_by_user(user_id)
        employee_1095c = Employee1095C.objects.filter(person=person.id, company=company_id)
        company_1095c = Company1095C.objects.filter(company=company_id)

        employee_1095c_collection = []
        for period in PERIODS:
            period_data = None
            if employee_1095c:
                period_data = next((datum for datum in employee_1095c if datum.period == period), None)
            else:
                period_data = next((datum for datum in company_1095c if datum.period == period), None)
            employee_1095c_data = Employee1095CData(period_data)
            employee_1095c_collection.append(employee_1095c_data)

        return employee_1095c_collection

    def _get_employee_i9_data(self, user_id):
        i9_model = None

        try:
            i9_model = EmploymentAuthorization.objects.get(user=user_id)
        except EmploymentAuthorization.DoesNotExist:
            i9_model = None

        if not i9_model:
            return None

        return EmployeeI9Data(i9_model)

    def _get_employee_w4_data(self, user_id):
        w4_model = None

        try:
            w4_model = W4.objects.get(user=user_id)
        except W4.DoesNotExist:
            w4_model = None

        if not w4_model:
            return None

        return EmployeeW4Data(w4_model)

    def _get_employee_state_tax_info(self, user_id):
        election_models = EmployeeStateTaxElection.objects.filter(user=user_id)
        return EmployeeStateTaxInfo(election_models)

    def _get_company_1094_c_data(self, company_id):
        member_info = None
        try:
            member_info = Company1094CMemberInfo.objects.get(company=company_id)
        except Company1094CMemberInfo.DoesNotExist:
            member_info = None
            
        monthly_info = Company1094CMonthlyMemberInfo.objects.filter(company=company_id)
        return Company1094CData(member_info, monthly_info, PERIODS)
