import json
import decimal
import traceback
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
            employee_data_dto = self._get_employee_data_dto(employee_user_id, external_company_id)

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

    def _update_employee_data_to_remote(self, employee_data_dto): 
        data = employee_data_dto.__dict__

        # [TODO]: Handle non-ok results
        response = self.web_request_service.put(
            self._cp_api_url,
            data_object=data,
            auth_token=self._cp_api_auth_token) 

    def _create_employee_data_to_remote(self, employee_data_dto):
        data = employee_data_dto.__dict__

        # [TODO]: Handle non-ok results
        response = self.web_request_service.post(
            self._cp_api_url,
            data_object=data,
            auth_token=self._cp_api_auth_token)

        # The body of the response is the payroll ID
        if (response.status_code == 200):
            return response.text

        return None

    def _get_cp_client_code_by_employee(self, employee_user_id):
        company_id = self.company_personnel_service.get_company_id_by_employee_user_id(employee_user_id)
        integration_providers = self.integration_provider_service.get_company_integration_providers(company_id)
        payroll_provider = integration_providers[self._integration_service_type()]
        if (payroll_provider is not None 
            and payroll_provider['integration_provider']['name'] == self._integration_provider_name()):
            return payroll_provider['company_external_id']

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
