import json
import decimal
import traceback
from dateutil.parser import parse
from django.contrib.auth import get_user_model

from app.factory.report_view_model_factory import ReportViewModelFactory
from app.service.company_personnel_service import CompanyPersonnelService
from app.service.web_request_service import WebRequestService
from app.service.integration.integration_provider_data_service_base import IntegrationProviderDataServiceBase
from app.service.integration.integration_provider_service import (
        INTEGRATION_SERVICE_TYPE_PAYROLL,
        INTEGRATION_PAYROLL_CONNECT_PAYROLL,
        IntegrationProviderService
    )
from app.service.system_settings_service import (
        SystemSettingsService,
        SYSTEM_SETTING_CPAPIAUTHTOKEN,
        SYSTEM_SETTING_CPAPIBASEURI,
        SYSTEM_SETTING_CPAPIEMPLOYEEROUTE
    )
from connect_payroll_employee_dto import ConnectPayrollEmployeeDto
from app.service.monitoring.logging_service import LoggingService

User = get_user_model()


class ConnectPayrollDataService(IntegrationProviderDataServiceBase):
    _logger = LoggingService()

    def __init__(self):
        super(ConnectPayrollDataService, self).__init__()
        self.view_model_factory = ReportViewModelFactory()
        self.web_request_service = WebRequestService()
        self.company_personnel_service = CompanyPersonnelService()
        self.integration_provider_service = IntegrationProviderService()

        # Retrieve the api token if available
        setting_service = SystemSettingsService()
        self._cp_api_auth_token = setting_service.get_setting_value_by_name(SYSTEM_SETTING_CPAPIAUTHTOKEN)

        # Also construct the API url, if available
        self._cp_api_url = None
        base_uri = setting_service.get_setting_value_by_name(SYSTEM_SETTING_CPAPIBASEURI)
        employee_route = setting_service.get_setting_value_by_name(SYSTEM_SETTING_CPAPIEMPLOYEEROUTE)
        if (base_uri and employee_route):
            self._cp_api_url = base_uri + employee_route

    def _integration_service_type(self):
        return INTEGRATION_SERVICE_TYPE_PAYROLL

    def _integration_provider_name(self):
        return INTEGRATION_PAYROLL_CONNECT_PAYROLL

    def _internal_generate_and_record_external_employee_number(self, employee_user_id):
        # First check whether the said employee already have a number
        # If so, this is an exception state, log it, and skip the operation
        employee_number = self.integration_provider_service.get_employee_integration_provider_external_id(
            employee_user_id,
            self._integration_service_type(),
            self._integration_provider_name())
        if (employee_number):
            logging.error('Invalid Operation: Try to generate external ID for employee (User ID={0}) already has one!'.format(employee_user_id))
            return

        company_id = self.company_personnel_service.get_company_id_by_employee_user_id(employee_user_id)
        next_employee_number = self._get_next_external_employee_number(company_id)
        # Now save the next usable external employee number to the profile
        # of the specified employee
        self._set_employee_external_id(
            employee_user_id,
            self._integration_service_type(),
            self._integration_provider_name(),
            next_employee_number
        )

    def _get_next_external_employee_number(self, company_id):
        return 0

    def _internal_sync_employee_data_to_remote(self, employee_user_id):
        # If the Connect Payroll API's auth token is not specified 
        # in the environment, consider this feature to be off, and 
        # skip all together.
        if (not self._cp_api_auth_token):
            return

        if (not self._cp_api_url):
            return

        # Also check whether the employee belong to a company with
        # the right setup with the remote system. And also skip if
        # this is not the case
        external_company_id = self._get_cp_client_code_by_employee(employee_user_id)
        if (not external_company_id):
            return

        try:
            # Populate the data object from the current state of the employee in WBM system
            # Also apply client(WBM) side validation on the data, based on understanding of
            # documentation from ConnectPay   
            employee_data_dto = self._get_employee_data_dto(employee_user_id, external_company_id)
            issue_list = self._validate_employee_data_dto(employee_data_dto)

            if (issue_list and len(issue_list) > 0):
                raise RuntimeError('There are problems collecting complete data required to sync to ConnectPay API for employee "{0}"'.format(employee_user_id), issue_list)

            if (employee_data_dto.payrollId):
                # Already exists in CP system, update
                self._logger.info('Updating Employee CP ID: ' + employee_data_dto.payrollId)
                self._logger.info(employee_data_dto)
                self._update_employee_data_to_remote(employee_data_dto)
            else:
                # Does not yet exist in CP system, new employee addition, create
                self._logger.info('Creating new employee record on CP system ...')
                self._logger.info(employee_data_dto)
                payroll_id = self._create_employee_data_to_remote(employee_data_dto)
                self._logger.info('Created Employee CP ID: {0}'.format(payroll_id))

                # Sync the cp ID from the response
                self._set_employee_external_id(
                        employee_user_id,
                        self._integration_service_type(),
                        self._integration_provider_name(),
                        payroll_id
                    )
        except Exception as e:
            self._logger.error(traceback.format_exc())
            raise

    def _get_employee_data_dto(self, employee_user_id, external_company_id):
        # First populate the CP identifiers
        dto = ConnectPayrollEmployeeDto()
        dto.payrollId = self._get_employee_external_id(
                employee_user_id,
                self._integration_service_type(),
                self._integration_provider_name()
            )
        dto.companyId = external_company_id

        # Now populate other data
        company_id = self.company_personnel_service.get_company_id_by_employee_user_id(employee_user_id)
        company_info = self.view_model_factory.get_company_info(company_id)
        person_info = self.view_model_factory.get_employee_person_info(employee_user_id)

        # Employee basic data
        dto.ssn = person_info.ssn
        dto.firstName = person_info.first_name
        dto.lastName = person_info.last_name
        dto.dob = self._get_date_string(person_info.birth_date)
        dto.gender = person_info.gender
        dto.address1 = person_info.address1
        dto.address2 = person_info.address2
        dto.city = person_info.city
        dto.country = person_info.country
        dto.state = person_info.state
        dto.zip = person_info.zipcode
        dto.email = person_info.email
        if (len(person_info.phones) > 0):
            dto.phone = person_info.phones[0]['number']

        # Employment data
        employee_profile_info = self.view_model_factory.get_employee_employment_profile_data(
                                    employee_user_id,
                                    company_info.company_id)

        if (employee_profile_info):
            dto.jobTitle = employee_profile_info.job_title
            dto.fullTime = employee_profile_info.is_full_time_employee()
            dto.hireDate = self._get_date_string(employee_profile_info.hire_date)
            dto.originalHireDate = self._get_date_string(employee_profile_info.hire_date)
            # [TODO]: Needs specification on employee status values
            dto.employeeStatus = '3'
            dto.terminationDate = self._get_date_string(employee_profile_info.end_date)

            # Salary data
            dto.payEffectiveDate = self._get_date_string(employee_profile_info.compensation_effective_date)
            dto.annualBaseSalary = self._get_decimal_string(employee_profile_info.annual_salary)
            dto.baseHourlyRate = self._get_decimal_string(employee_profile_info.current_hourly_rate)
            dto.hoursPerWeek = self._get_decimal_string(employee_profile_info.projected_hours_per_week)  

        # Other
        employee_i9_info = self.view_model_factory.get_employee_i9_data(employee_user_id)
        if (employee_i9_info):
            self.usCitizen = employee_i9_info.citizen_data is not None

        return dto

    def _validate_employee_data_dto(self, employee_data_dto):
        issue_list = []

        # System Data
        _DataValidator(employee_data_dto, 'companyId', issue_list) \
            .with_value_exists_check() \
            .with_value_length_check(6, 6) \
            .validate()

        _DataValidator(employee_data_dto, 'payrollId', issue_list) \
            .with_value_valid_integer_check() \
            .validate()

        # Employee bio data and basic info
        _DataValidator(employee_data_dto, 'ssn', issue_list) \
            .with_value_exists_check() \
            .with_value_length_check(9, 9) \
            .validate()

        _DataValidator(employee_data_dto, 'firstName', issue_list) \
            .with_value_exists_check() \
            .with_value_length_check(1, 20) \
            .validate()

        _DataValidator(employee_data_dto, 'middleName', issue_list) \
            .with_value_length_check(0, 20) \
            .validate()

        _DataValidator(employee_data_dto, 'lastName', issue_list) \
            .with_value_exists_check() \
            .with_value_length_check(1, 20) \
            .validate()

        _DataValidator(employee_data_dto, 'dob', issue_list) \
            .with_value_exists_check() \
            .with_value_valid_datetime_check() \
            .validate()

        _DataValidator(employee_data_dto, 'gender', issue_list) \
            .with_value_exists_check() \
            .with_value_in_list_check(['M', 'F']) \
            .validate()

        _DataValidator(employee_data_dto, 'address1', issue_list) \
            .with_value_length_check(0, 30) \
            .validate()

        _DataValidator(employee_data_dto, 'address2', issue_list) \
            .with_value_length_check(0, 30) \
            .validate()

        _DataValidator(employee_data_dto, 'city', issue_list) \
            .with_value_length_check(0, 28) \
            .validate()

        _DataValidator(employee_data_dto, 'state', issue_list) \
            .with_value_exists_check() \
            .with_value_length_check(2, 2) \
            .validate()

        _DataValidator(employee_data_dto, 'zip', issue_list) \
            .with_value_exists_check() \
            .with_value_length_check(5, 10) \
            .validate()

        _DataValidator(employee_data_dto, 'country', issue_list) \
            .with_value_length_check(0, 30) \
            .validate()

        _DataValidator(employee_data_dto, 'email', issue_list) \
            .with_value_exists_check() \
            .with_value_length_check(1, 250) \
            .validate()

        _DataValidator(employee_data_dto, 'phone', issue_list) \
            .with_value_length_check(0, 14) \
            .validate()

        _DataValidator(employee_data_dto, 'phone', issue_list) \
            .with_value_length_check(0, 14) \
            .validate()

        # Employment data
        _DataValidator(employee_data_dto, 'department', issue_list) \
            .with_value_valid_integer_check() \
            .validate()

        _DataValidator(employee_data_dto, 'division', issue_list) \
            .with_value_valid_integer_check() \
            .validate()

        _DataValidator(employee_data_dto, 'union', issue_list) \
            .with_value_type_boolean_check() \
            .validate()

        _DataValidator(employee_data_dto, 'jobTitle', issue_list) \
            .with_value_length_check(0, 30) \
            .validate()

        _DataValidator(employee_data_dto, 'fullTime', issue_list) \
            .with_value_type_boolean_check() \
            .validate()

        _DataValidator(employee_data_dto, 'seasonal', issue_list) \
            .with_value_type_boolean_check() \
            .validate()

        _DataValidator(employee_data_dto, 'hireDate', issue_list) \
            .with_value_exists_check() \
            .with_value_valid_datetime_check() \
            .validate()

        _DataValidator(employee_data_dto, 'originalHireDate', issue_list) \
            .with_value_valid_datetime_check() \
            .validate()

        _DataValidator(employee_data_dto, 'terminationDate', issue_list) \
            .with_value_valid_datetime_check() \
            .validate()

        self.employeeStatus = None

        # Salary data
        _DataValidator(employee_data_dto, 'payEffectiveDate', issue_list) \
            .with_value_valid_datetime_check() \
            .validate()

        _DataValidator(employee_data_dto, 'annualBaseSalary', issue_list) \
            .with_value_valid_decimal_check() \
            .validate()

        _DataValidator(employee_data_dto, 'baseHourlyRate', issue_list) \
            .with_value_valid_decimal_check() \
            .validate()

        return issue_list

    def _update_employee_data_to_remote(self, employee_data_dto): 
        data = employee_data_dto.__dict__

        response = self.web_request_service.put(
            self._cp_api_url,
            data_object=data,
            auth_token=self._cp_api_auth_token)

        response.raise_for_status()

    def _create_employee_data_to_remote(self, employee_data_dto):
        data = employee_data_dto.__dict__

        response = self.web_request_service.post(
            self._cp_api_url,
            data_object=data,
            auth_token=self._cp_api_auth_token)

        response.raise_for_status()

        # Also, we really only expect here the below based on CP API behavior
        # * HTTP 200
        # * body contains the resultant ID created 
        # So throw if we receive anything else
        if (response.status_code != 200):
            raise RuntimeError('POST to ConnectPay Employee API resulted in a non-200 status: "{0}"'.format(response.status_code), response)

        if (not response.text):
            raise RuntimeError('POST to ConnectPay Employee API resulted in empty body, and hence was not able to receive new employee ID.')

        return response.text

    def _get_cp_client_code_by_employee(self, employee_user_id):
        company_id = self.company_personnel_service.get_company_id_by_employee_user_id(employee_user_id)
        
        if (company_id):
            return self.integration_provider_service.get_company_integration_provider_external_id(
                company_id,
                self._integration_service_type(),
                self._integration_provider_name())

        return None

    def _get_date_string(self, date):
        if date:
            try:
                return date.isoformat()
            except:
                return None
        else:
            return None

    def _get_decimal_string(self, input_value):
        if isinstance(input_value, decimal.Decimal):
            return str(input_value)

        return input_value


class _DataValidator(object):
    def __init__(self, dto, field_name, issue_list):
        dto_dict = dto.__dict__
        if (field_name not in dto_dict):
            raise RuntimeError('The specified field name to check is not part of the object.')
        self._field_value = dto_dict[field_name]
        self._field_name = field_name
        self._issue_list = issue_list
        self._check_list = []

    def with_value_exists_check(self):
        self._check_list.append(lambda : self.__check_value_exists())
        return self

    def with_value_length_check(self, min_length, max_length):
        self._check_list.append(lambda : self.__check_value_length(min_length, max_length))
        return self

    def with_value_type_boolean_check(self):
        self._check_list.append(lambda : self.__check_value_type_boolean())
        return self

    def with_value_valid_integer_check(self):
        self._check_list.append(lambda : self.__check_value_valid_integer())
        return self

    def with_value_valid_datetime_check(self):
        self._check_list.append(lambda : self.__check_value_valid_datetime())
        return self

    def with_value_valid_decimal_check(self):
        self._check_list.append(lambda : self.__check_value_valid_decimal())
        return self

    def with_value_in_list_check(self, value_list):
        self._check_list.append(lambda : self.__check_value_in_list(value_list))
        return self

    def validate(self):
        for check in self._check_list:
            check()

    def __append_issue(self, issue):
        prefix_token = '[Field="{0}" | Value="{1}"]'.format(self._field_name, self._field_value)
        self._issue_list.append('{0} {1}'.format(prefix_token, issue))

    def __check_value_exists(self):
        if (not self._field_value):
            self.__append_issue('Missing value for required field')

    def __check_value_length(self, min_length, max_length):
        if (min_length < 0 or max_length < 0 or max_length < min_length):
            raise ValueError('The provided min_length and max_length to check is not valid: "[{0}, {1}]"'.format(min_length, max_length))
        if (not self._field_value):
            return
        value_len = len(self._field_value)
        if (value_len < min_length or value_len > max_length):
            self.__append_issue('Value length out of expected range: excepted-"[{0}, {1}]", was-"{2}"'.format(min_length, max_length, value_len))

    def __check_value_type_boolean(self):
        if (not self._field_value):
            return
        if (not isinstance(self._field_value, bool)):
            self.__append_issue('Value is not of expected type "boolean"')

    def __check_value_valid_integer(self):
        if (not self._field_value):
            return
        if (not self.__is_integer(self._field_value)):
            self.__append_issue('Value is not of expected type "integer"')

    def __check_value_valid_decimal(self):
        if (not self._field_value):
            return
        if (not self.__is_decimal(self._field_value)):
            self.__append_issue('Value is not valid decimal string')

    def __check_value_valid_datetime(self):
        if (not self._field_value):
            return
        if (not self.__is_datetime(self._field_value)):
            self.__append_issue('Value is not valid date time string')

    def __check_value_in_list(self, value_list):
        if (not self._field_value):
            return
        if (not value_list or not isinstance(value_list, list)):
            raise ValueError('Provided value_list is not valid')
        if (not self._field_value in value_list):
            self.__append_issue('Value is outside expected options: "{0}"'.format(value_list))

    def __is_datetime(self, date_string):
        try: 
            parse(date_string)
            return True
        except ValueError:
            return False

    def __is_decimal(self, decimal_value):
        if (isinstance(decimal_value, float)):
            return True

        try: 
            float(decimal_value)
            return True
        except ValueError:
            return False

    def __is_integer(self, integer_value):
        # Note: python considers boolean values True/False to be integer type
        #       so needs to handle this case explicitly
        if (isinstance(integer_value, int)
            and not isinstance(integer_value, bool)):
            return True

        try:
            int(integer_value)
            return True
        except ValueError:
            return False
