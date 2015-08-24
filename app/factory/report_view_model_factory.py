from app.models.company_user import CompanyUser
from app.models.person import Person, SELF

from app.view_models.report.person_info import PersonInfo
from app.view_models.report.company_info import CompanyInfo


class ReportViewModelFactory(object):
    def get_employee_person_info(self, employee_user_id):
        return PersonInfo(self._get_person_by_user(employee_user_id))

    def get_employee_company_info(self, employee_user_id):
        return CompanyInfo(self._get_company_by_user(employee_user_id))

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
