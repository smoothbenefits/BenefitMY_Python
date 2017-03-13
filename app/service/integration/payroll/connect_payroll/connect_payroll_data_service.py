from django.contrib.auth import get_user_model

from app.factory.report_view_model_factory import ReportViewModelFactory
from app.service.web_request_service import WebRequestService
from app.service.integration.integration_provider_data_service_base import IntegrationProviderDataServiceBase
from app.service.integration.integration_provider_service import (
        INTEGRATION_SERVICE_TYPE_PAYROLL,
        INTEGRATION_PAYROLL_CONNECT_PAYROLL
    )

User = get_user_model()

# For now track the remote integration server here
# When this is officialized, keep it in settings
CONNECT_PAYROLL_API_BASE_URL = 'https://agilepayrollapi.azurewebsites.net/api/'
CONNECT_PAYROLL_API_EMPLOYEE_ROUTE = 'employee'

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

    def sync_employee_data_to_remote(self, employee_user_id):
        employee_cp_id = self._get_employee_external_id(
                employee_user_id,
                INTEGRATION_SERVICE_TYPE_PAYROLL,
                INTEGRATION_PAYROLL_CONNECT_PAYROLL
            )
        employee_data_dto = self._get_employee_data_dto(employee_user_id)

        if (employee_cp_id):
            # Already exists in CP system, update
            print 'Updating Employee...'
        else:
            # Does not yet exist in CP system, new employee addition, create
            print 'Creating Employee...'

        # Sync the cp ID from the response
        self._set_employee_external_id(
                employee_user_id,
                INTEGRATION_SERVICE_TYPE_PAYROLL,
                INTEGRATION_PAYROLL_CONNECT_PAYROLL,
                'ALibaba-Test'
            )

        return

    def _get_employee_data_dto(self, employee_user_id):
        return

    def _get_cp_client_code_by_employee(self, employee_user_id):
        # [TODO]: This should query for the actual client code
        #         via company's service provider relational data
        return TEST_CP_CLIENT_CODE
