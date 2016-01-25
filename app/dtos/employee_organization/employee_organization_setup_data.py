from app.models.employee_profile import EmployeeProfile
from app.models.person import Person

class EmployeeOrganizationSetupData(object):
    def __init__(
        self,
        employee_person_id=None,
        employee_first_name=None,
        employee_last_name=None,
        company_id=None,
        manager_profile_id=None,
        manager_first_name=None,
        manager_last_name=None):
        self.employee_person_id = employee_person_id
        self.employee_first_name = employee_first_name
        self.employee_last_name = employee_last_name
        self.company_id = company_id
        self.manager_profile_id = manager_profile_id
        self.manager_first_name = manager_first_name
        self.manager_last_name = manager_last_name

        # Revalidate the person_id
        employee_person = self.get_employee_person()
        if (employee_person):
            self.employee_person_id = employee_person.id
        else:
            self.employee_person_id = None

        manager_profile = self.get_manager_profile()
        if (manager_profile):
            self.manager_profile_id = manager_profile.id
        else:
            self.manager_profile_id = None

    def has_manager_info_specified(self):
        if (self.manager_profile_id
            or self.manager_first_name
            or self.manager_last_name):
            return True
        return False

    def get_employee_person(self):
        employee_profile = self.get_employee_profile()
        if (employee_profile):
            return employee_profile.person
        return None

    def get_employee_profile(self):
        if (self.employee_person_id):
            try:
                return EmployeeProfile.objects.get(
                    person=self.employee_person_id,
                    company=self.company_id)
            except EmployeeProfile.DoesNotExist:
                return None
        elif (self.employee_first_name and self.employee_last_name):
            employee_profile = self._get_employee_profile_by_name_and_company(
                self.employee_first_name,
                self.employee_last_name,
                self.company_id)
            if (employee_profile):
                return employee_profile
        return None

    def get_manager_profile(self):
        if (self.manager_profile_id):
            try:
                return EmployeeProfile.objects.get(pk=self.manager_profile_id)
            except EmployeeProfile.DoesNotExist:
                return None
        elif (self.manager_first_name and self.manager_last_name):
            return self._get_employee_profile_by_name_and_company(
                self.manager_first_name,
                self.manager_last_name,
                self.company_id)
        return None

    def _get_employee_profile_by_name_and_company(self, first_name, last_name, company_id):
        try:
            return EmployeeProfile.objects.get(
                    company=company_id,
                    person__first_name=first_name,
                    person__last_name=last_name)
        except EmployeeProfile.DoesNotExist:
            return None
