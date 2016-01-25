from datetime import datetime
from StringIO import StringIO
from django.contrib.auth import get_user_model

from app.models.employee_profile import EmployeeProfile
from app.dtos.operation_result import OperationResult
from app.dtos.employee_organization.employee_organization_setup_data \
    import EmployeeOrganizationSetupData
from app.serializers.employee_organization.employee_organization_setup_data_serializer \
    import EmployeeOrganizationSetupDataSerializer, EmployeeOrganizationSetupDataPostSerializer

User = get_user_model()


class EmployeeOrganizationService(object):
    FIELD_FIRST_NAME = 'first_name'
    FIELD_LAST_NAME = 'last_name'
    FIELD_MANAGER_FIRST_NAME = 'manager_first_name'
    FIELD_MANAGER_LAST_NAME = 'manager_last_name'
    FIELD_RECORD_END = 'record-end'

    REQUIRED_RAW_DATA_FIELDS = [
        FIELD_FIRST_NAME,
        FIELD_LAST_NAME,
        FIELD_MANAGER_FIRST_NAME,
        FIELD_MANAGER_LAST_NAME,
        FIELD_RECORD_END
    ]

    def parse_batch_employee_organization_import_raw_data(self, batch_import_raw_data):
        result = OperationResult(batch_import_raw_data)
        parsed_org_data_list = []

        # check all lines for number of fields
        # if found bad ones, send the main wrapper back without
        # construting the individual ones
        for line in batch_import_raw_data.raw_data.split('\n'):
            if (not line.strip()):
                continue

            tokens = line.split('\t')

            if (len(tokens) != len(self.REQUIRED_RAW_DATA_FIELDS)):
                result.append_issue(
                    'The line [%s] fails to parse properly. Reason: Do not have enough number of fields' % line
                )
            else:

                # parse the fields into domain object and 
                # construct the DTO needed
                org_data = {
                    'company_id': batch_import_raw_data.company_id,
                    'employee_first_name': self._get_field_value(tokens, self.FIELD_FIRST_NAME),
                    'employee_last_name': self._get_field_value(tokens, self.FIELD_LAST_NAME),
                    'manager_first_name': self._get_field_value(tokens, self.FIELD_MANAGER_FIRST_NAME),
                    'manager_last_name': self._get_field_value(tokens, self.FIELD_MANAGER_LAST_NAME)
                }

                # Parse the line into objects
                # Utilize serializers to perform all the details
                serializer = EmployeeOrganizationSetupDataPostSerializer(data=org_data)

                if (not serializer.is_valid()):
                    result.append_issue(
                        'The line [%s] fails to parse properly. Reasons:[%s]' % (line, serializer.errors)
                    )
                else:
                    parsed_org_data_list.append(serializer.object)

        # Do batch validation,
        #  - Collect batch level issues into the result
        #  - include the list of validated account data as output
        batch_validation_result = self.batch_validate_employee_organization_setup_data(parsed_org_data_list)
        batch_validation_result.copy_issues_to(result)
        result.set_output_data(batch_validation_result.output_data)

        return result

    def _get_field_value(self, field_values, field_name):
        index = self.REQUIRED_RAW_DATA_FIELDS.index(field_name)
        if (index < 0 or index >= len(field_values)):
            return None
        return field_values[index]

    def batch_execute_employee_organization_setup(self, organization_setup_data_list):
        result = self.batch_validate_employee_organization_setup_data(
            organization_setup_data_list)

        if (result.has_issue()):
            raise Exception(
                "Encountered validation issues while executing batch employee organization setup!")

        execute_results = []

        # Batch process
        for data in organization_setup_data_list:
            execute_result = self.execute_employee_organization_setup(data, False)
            execute_results.append(execute_result)

        result.set_output_data(execute_results)
        return result

    def execute_employee_organization_setup(self, organization_setup_data, do_validation=True):
        result = None

        # Do validation first, and short circuit if failed
        if (do_validation):
            result = self._validate_employee_organization_setup_data(organization_setup_data)
        else:
            # directly construct the result, skipping validation
            result = OperationResult(organization_setup_data)

        # If the operation input info is not valid to begin with
        # simply short circuit and return it
        if (result.has_issue()):
            raise Exception(
                "Encountered validation issues while executing employee organization setup!")

        # get employee profile to update
        employee_profile = organization_setup_data.get_employee_profile()

        # get manager's profile
        manager_profile = organization_setup_data.get_manager_profile()

        # now do the assignment
        employee_profile.manager = manager_profile
        employee_profile.save()

    def batch_validate_employee_organization_setup_data(self, organization_setup_data_list):
        result = OperationResult(organization_setup_data_list)

        if (not organization_setup_data_list):
            result.append_issue(
                'Did not find any employee organization setup to handle'
            )
        else:
            has_invalid = False
            validation_results = []

            for data in organization_setup_data_list:
                validate_result = self._validate_employee_organization_setup_data(data)
                if (validate_result.has_issue()):
                    has_invalid = True   

                validation_results.append(validate_result)

            if (has_invalid):
                result.append_issue(
                    'There are validation issues on some employee organization setup data.'
                )

            result.set_output_data(validation_results)

        return result

    def _validate_employee_organization_setup_data(self, organization_setup_data):
        result = OperationResult(organization_setup_data)
        result.set_output_data(organization_setup_data)

        if (not organization_setup_data or
            not organization_setup_data.company_id):
            result.append_issue(
                "Missing necessary information for employee organization setup"
            )
            return result

        if (not organization_setup_data.employee_person_id):
            result.append_issue(
                "Could not locate employee profile for the given employee"
            )

        # It is a valid case where manager info is not specified, which 
        # we infer as to not-setup or remove manager for the employee
        # But it is invalid that the manager info is specified but failed
        # to resolve to a valid employee profile
        if (organization_setup_data.has_manager_info_specified() 
            and not organization_setup_data.manager_profile_id):
            result.append_issue(
                "Could not locate manager's employee profile based on info provided"
            )

        # check the employee and manager belong to the same company
        employee_profile = organization_setup_data.get_employee_profile()
        manager_profile = organization_setup_data.get_manager_profile()
        if (employee_profile and manager_profile):
            if (employee_profile.company.id != manager_profile.company.id):
                result.append_issue(
                    "The employee and manager specified do not work in the same company"
                )

        return result
