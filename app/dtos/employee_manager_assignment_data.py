class EmployeeManagerAssignmentData(object):
    def __init__(
        self,
        employee_person_id=None,
        company_id=None,
        manager_profile_id=None,
        manager_first_name=None,
        manager_last_name=None):
        self.employee_person_id = employee_person_id
        self.company_id = company_id
        self.manager_profile_id = manager_profile_id
        self.manager_first_name = manager_first_name
        self.manager_last_name = manager_last_name
