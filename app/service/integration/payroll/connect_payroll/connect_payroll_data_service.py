import json
from django.contrib.auth import get_user_model

from app.factory.report_view_model_factory import ReportViewModelFactory
from app.service.company_personnel_service import CompanyPersonnelService
from app.service.web_request_service import WebRequestService
from app.service.integration.integration_provider_data_service_base import IntegrationProviderDataServiceBase
from app.service.integration.integration_provider_service import (
        INTEGRATION_SERVICE_TYPE_PAYROLL,
        INTEGRATION_PAYROLL_CONNECT_PAYROLL
    )
from connect_payroll_employee_dto import ConnectPayrollEmployeeDto

User = get_user_model()

# For now track the remote integration server here
# When this is officialized, keep it in settings
CONNECT_PAYROLL_API_BASE_URL = 'https://agilepayrollapi.azurewebsites.net/api/employee-navigator/'
CONNECT_PAYROLL_API_EMPLOYEE_ROUTE = 'employees'

# For testing purpose, put the below constants here
# These should be modeled in data model, and retrieved as such.
TEST_CP_CLIENT_CODE = '739600'

# Hand shake protocal to get API key/authentication token 
# needs to be figured out with CP. 
# Hard code for testing purpose for now
CONNECT_PAYROLL_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6IlN3YWdnZXIiLCJyb2xlIjoiRGV2ZWxvcGVyIiwibmJmIjoxNDg5MTY1NjM3LCJleHAiOjE0ODk3NzA0MzcsImlhdCI6MTQ4OTE2NTYzNywiaXNzIjoiaHR0cHM6Ly9hZ2lsZXBheXJvbGxhcGkuYXp1cmV3ZWJzaXRlcy5uZXQvIiwiYXVkIjoiaHR0cHM6Ly9hZ2lsZXBheXJvbGxhcGkuYXp1cmV3ZWJzaXRlcy5uZXQvIn0.32i4TugLUlzCB8S9z47zfYOkKHqUnm3SfEr6SFXilWI'


class ConnectPayrollDataService(IntegrationProviderDataServiceBase):

    def __init__(self):
        super(ConnectPayrollDataService, self).__init__()
        self.view_model_factory = ReportViewModelFactory()
        self.web_request_service = WebRequestService()
        self.company_personnel_service = CompanyPersonnelService()

    def sync_employee_data_to_remote(self, employee_user_id):
        employee_data_dto = self._get_employee_data_dto(employee_user_id)

        if (employee_data_dto.payrollId):
            # Already exists in CP system, update
            print 'Updating Employee...'
            self._update_employee_data_to_remote(employee_data_dto)
        else:
            # Does not yet exist in CP system, new employee addition, create
            print 'Creating Employee...'
            payroll_id = self._create_employee_data_to_remote(employee_data_dto)
            # Sync the cp ID from the response
            self._set_employee_external_id(
                    employee_user_id,
                    INTEGRATION_SERVICE_TYPE_PAYROLL,
                    INTEGRATION_PAYROLL_CONNECT_PAYROLL,
                    payroll_id
                )

    def _get_employee_data_dto(self, employee_user_id):
        # First populate the CP identifiers
        dto = ConnectPayrollEmployeeDto()
        dto.payrollId = self._get_employee_external_id(
                employee_user_id,
                INTEGRATION_SERVICE_TYPE_PAYROLL,
                INTEGRATION_PAYROLL_CONNECT_PAYROLL
            )
        if (dto.payrollId == 'ALibaba-Test'):
            dto.payrollId = None
        dto.companyId = self._get_cp_client_code_by_employee(employee_user_id)
        
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
            dto.employeeStatus = 3
            dto.terminationDate = self._get_date_string(employee_profile_info.end_date)

            # Salary data
            self.payEffectiveDate = self._get_date_string(employee_profile_info.compensation_effective_date)
            self.annualBaseSalary = employee_profile_info.annual_salary
            self.baseHourlyRate = employee_profile_info.current_hourly_rate
            self.hoursPerWeek = employee_profile_info.projected_hours_per_week  

        # Other
        employee_i9_info = self.view_model_factory.get_employee_i9_data(employee_user_id)
        if (employee_i9_info):
            self.usCitizen = employee_i9_info.citizen_data is not None

        return dto

    def _update_employee_data_to_remote(self, employee_data_dto): 
        api_url = self._get_employee_api_url()
        data = employee_data_dto.__dict__

        # [TODO]: Handle non-ok results
        response = self.web_request_service.put(
            api_url,
            data_object=data,
            auth_token=CONNECT_PAYROLL_API_KEY) 

    def _create_employee_data_to_remote(self, employee_data_dto):
        api_url = self._get_employee_api_url()
        data = employee_data_dto.__dict__

        # [TODO]: Handle non-ok results
        response = self.web_request_service.post(
            api_url,
            data_object=data,
            auth_token=CONNECT_PAYROLL_API_KEY)

        # The body of the response is the payroll ID
        if (response.status_code == 200):
            return response.text

        return None

    def _get_cp_client_code_by_employee(self, employee_user_id):
        # [TODO]: This should query for the actual client code
        #         via company's service provider relational data
        return TEST_CP_CLIENT_CODE

    def _get_employee_api_url(self):
        return CONNECT_PAYROLL_API_BASE_URL + CONNECT_PAYROLL_API_EMPLOYEE_ROUTE

    def _get_date_string(self, date):
        if date:
            try:
                return date.isoformat()
            except:
                return None
        else:
            return None