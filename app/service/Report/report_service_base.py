from app.models.company_user import CompanyUser
from app.models.person import Person
from app.models.direct_deposit import DirectDeposit
from app.models.employee_profile import EmployeeProfile


class ReportServiceBase(object):

    _user_employee_profile_dictionary = {}

    def _get_employee_profile_by_user_id(self, user_id, company_id):
        if user_id not in self._user_employee_profile_dictionary:
            try:
                person = Person.objects.filter(user=user_id, relationship='self')
                profiles = EmployeeProfile.objects.filter(person=person, company=company_id)
                if profiles:
                    self._user_employee_profile_dictionary[user_id] = profiles[0]
                else:
                    self._user_employee_profile_dictionary[user_id] = None;
            except Person.DoesNotExist:
                return None;
        return self._user_employee_profile_dictionary[user_id]


    def _get_max_dependents_count(self, company_id):
        user_ids = self._get_all_employee_user_ids_for_company(company_id)
        persons = Person.objects.filter(user__in=user_ids).exclude(relationship='self').exclude(relationship='spouse')

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
        user_ids = []
        users = CompanyUser.objects.filter(company=company_id,
                                           company_user_type='employee')
        for user in users:
            user_ids.append(user.user_id)

        return user_ids

    def _get_company_by_user(self, user_id):
        company_model = None

        companies = CompanyUser.objects.filter(user=user_id)
        if (len(companies) > 0):
            company_model = companies[0].company

        return company_model

    def _get_date_string(self, date):
        if date:
            try:
                return date.strftime("%m/%d/%Y")
            except:
                return ''
        else:
            return ''

    def _get_date_time_string(self, date):
        if date:
            try:
                return date.strftime("%m/%d/%Y %H:%M:%S")
            except:
                return ''
        else:
            return ''
