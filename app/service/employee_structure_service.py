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
    def batch_manager_assignments(self, employee_manager_assignment_data_list):
        result = self._batch_validate_manager_assignment_data(
            employee_manager_assignment_data_list)

        if (result.has_issue()):
            return result

        assignment_results = []

        # Create all employee accounts
        for assignment_data in employee_manager_assignment_data_list:
            assignment_result = self.assign_manager_for_employee(assignment_data, False)
            assignment_results.append(assignment_result)

        result.set_output_data(assignment_results)
        return result

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

    def _batch_validate_manager_assignment_data(self, employee_manager_assignment_data_list):
        result = OperationResult(employee_manager_assignment_data_list)

        if (not employee_manager_assignment_data_list):
            result.append_issue(
                'Did not find any manager assignment info to handle'
            )
        else:
            has_invalid = False
            assignment_validation_results = []

            for assignment_data in employee_manager_assignment_data_list:
                validate_result = self._validate_manager_assignment_data(assignment_data)
                if (validate_result.has_issue()):
                    has_invalid = True

                assignment_validation_results.append(validate_result)

            if (has_invalid):
                result.append_issue(
                    'There are validation issues on some manager assignment info.'
                )

            result.set_output_data(assignment_validation_results)

        return result

    def _validate_manager_assignment_data(self, employee_manager_assignment_data):
        result = OperationResult(employee_manager_assignment_data)
        result.set_output_data(employee_manager_assignment_data)

        incomplete_manager_name_info = (
            not employee_manager_assignment_data.manager_first_name
            or not employee_manager_assignment_data.manager_last_name)

        # Require either to provide manager's profile ID or the full name data
        incomplete_manager_info = (
            not employee_manager_assignment_data.manager_profile_id
            and incomplete_manager_name_info)

        if (not employee_manager_assignment_data or
            not employee_manager_assignment_data.company_id or
            not employee_manager_assignment_data.employee_person_id or
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
        if (not manager_profile):
            result.append_issue(
                "Could not locate manager's employee profile based on info provided"
            )

        return result

    def _get_manager_employee_profile(self, employee_manager_assignment_data):
        if (employee_manager_assignment_data.manager_profile_id):
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
