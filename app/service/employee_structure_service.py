from datetime import datetime
from StringIO import StringIO
from django.contrib.auth import get_user_model
from django import template
from django.core.mail import send_mail
from django.conf import settings

from app.models.employee_profile import EmployeeProfile
from app.dtos.operation_result import OperationResult

User = get_user_model()


class EmployeeStructureService(object):
    def assign_manager_for_employee(self, employee_manager_assignment_data, do_validation=True):
        result = None

        # Do validation first, and short circuit if failed
        if (do_validation):
            result = self._validate_manager_assignment_data(employee_manager_assignment_data)
        else:
            # directly construct the result, skipping validation
            result = OperationResult(employee_manager_assignment_data)

        # If the operation input info is not valid to begin with
        # simply short circuit and return it
        if (result.has_issue()):
            return result

        # get employee profile to update
        employee_profile = EmployeeProfile.objects.get(
                person=employee_manager_assignment_data.employee_person_id,
                company=employee_manager_assignment_data.company_id)

        # get manager's profile
        manager_profile = self._get_manager_employee_profile(employee_manager_assignment_data)

        # now do the assignment
        employee_profile.manager = manager_profile
        employee_profile.save()

    def _validate_manager_assignment_data(self, employee_manager_assignment_data):
        result = OperationResult(employee_manager_assignment_data)
        result.set_output_data(employee_manager_assignment_data)

        incomplete_manager_name_info = (
            employee_manager_assignment_data.manager_first_name is None 
            or employee_manager_assignment_data.manager_last_name is None)

        # Require either to provide manager's profile ID or the full name data
        incomplete_manager_info = (
            employee_manager_assignment_data.manager_profile_id is None
            and incomplete_manager_name_info)

        if (employee_manager_assignment_data is None or
            employee_manager_assignment_data.company_id is None or
            employee_manager_assignment_data.employee_person_id is None or
            incomplete_manager_info):
            result.append_issue(
                "Missing necessary information for manager assignment"
            )
            return result

        try:
            EmployeeProfile.objects.get(
                person=employee_manager_assignment_data.employee_person_id,
                company=employee_manager_assignment_data.company_id)
        except EmployeeProfile.DoesNotExist:
            result.append_issue(
                "Could not locate employee profile for the given employee"
            )

        # now try get manager's employee profile
        manager_profile = self._get_manager_employee_profile(employee_manager_assignment_data)
        if (manager_profile is None):
            result.append_issue(
                "Could not locate manager's employee profile based on info provided"
            )

        return result

    def _get_manager_employee_profile(self, employee_manager_assignment_data):
        if (employee_manager_assignment_data.manager_profile_id is not None):
            try:
                return EmployeeProfile.objects.get(pk=employee_manager_assignment_data.manager_profile_id)
            except EmployeeProfile.DoesNotExist:
                return None
        else:
            # Try look up the employee profile by manager's full name
            try:
                return EmployeeProfile.objects.get(
                    company=employee_manager_assignment_data.company_id,
                    person__first_name=employee_manager_assignment_data.manager_first_name,
                    person__last_name=employee_manager_assignment_data.manager_last_name)
            except EmployeeProfile.DoesNotExist:
                return None
