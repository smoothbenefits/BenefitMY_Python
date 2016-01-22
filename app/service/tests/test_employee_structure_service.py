import re
from django.test import TestCase
from app.service.employee_structure_service import EmployeeStructureService
from app.dtos.employee_manager_assignment_data import EmployeeManagerAssignmentData
from app.models.employee_profile import EmployeeProfile
from app.models.person import Person


class TestEmployeeStructureService(TestCase):

    # your fixture files here
    fixtures = ['24_person', '49_period_definition', '10_company', '23_auth_user',
                'employee_profile', '11_address', '12_phone']

    def test_assign_manager_to_employee_manager_profile_id_succeed(self):
        service = EmployeeStructureService()

        person_id = 4
        company_id = 1
        manager_profile_id = 1
        manager_first_name = None
        manager_last_name = None

        data = EmployeeManagerAssignmentData(
            person_id,
            company_id,
            manager_profile_id,
            manager_first_name,
            manager_last_name
        )

        service.assign_manager_for_employee(data)

        employee_profile = EmployeeProfile.objects.get(person=person_id, company=company_id)

        self.assertEqual(employee_profile.manager.id, manager_profile_id)

    def test_assign_manager_to_employee_manager_full_name_succeed(self):
        service = EmployeeStructureService()

        manager_person_id = 3
        manager_person = Person.objects.get(pk=manager_person_id)

        person_id = 4
        company_id = 1
        manager_profile_id = None
        manager_first_name = manager_person.first_name
        manager_last_name = manager_person.last_name

        data = EmployeeManagerAssignmentData(
            person_id,
            company_id,
            manager_profile_id,
            manager_first_name,
            manager_last_name
        )

        service.assign_manager_for_employee(data)

        employee_profile = EmployeeProfile.objects.get(person=person_id, company=company_id)

        self.assertEqual(employee_profile.manager.id, manager_person.employee_profile_person.first().id)

    def test_assign_manager_to_employee_non_exist_employee_fail_with_validation_issue(self):
        service = EmployeeStructureService()

        person_id = 9999
        company_id = 1
        manager_profile_id = 1
        manager_first_name = None
        manager_last_name = None

        data = EmployeeManagerAssignmentData(
            person_id,
            company_id,
            manager_profile_id,
            manager_first_name,
            manager_last_name
        )

        result = service.assign_manager_for_employee(data)

        self.assertTrue(result.has_issue())

    def test_assign_manager_to_employee_non_exist_manager_by_profile_id_fail_with_validation_issue(self):
        service = EmployeeStructureService()

        person_id = 4
        company_id = 1
        manager_profile_id = 9999
        manager_first_name = None
        manager_last_name = None

        data = EmployeeManagerAssignmentData(
            person_id,
            company_id,
            manager_profile_id,
            manager_first_name,
            manager_last_name
        )

        result = service.assign_manager_for_employee(data)

        self.assertTrue(result.has_issue())

    def test_assign_manager_to_employee_non_exist_manager_by_name_fail_with_validation_issue(self):
        service = EmployeeStructureService()

        person_id = 4
        company_id = 1
        manager_profile_id = None
        manager_first_name = 'FirstName'
        manager_last_name = 'LastName'

        data = EmployeeManagerAssignmentData(
            person_id,
            company_id,
            manager_profile_id,
            manager_first_name,
            manager_last_name
        )

        result = service.assign_manager_for_employee(data)

        self.assertTrue(result.has_issue())

    def test_assign_manager_to_employee_incomplete_manager_name_fail_with_validation_issue(self):
        service = EmployeeStructureService()

        person_id = 4
        company_id = 1
        manager_profile_id = None
        manager_first_name = 'FirstName'
        manager_last_name = None

        data = EmployeeManagerAssignmentData(
            person_id,
            company_id,
            manager_profile_id,
            manager_first_name,
            manager_last_name
        )

        result = service.assign_manager_for_employee(data)

        self.assertTrue(result.has_issue())
