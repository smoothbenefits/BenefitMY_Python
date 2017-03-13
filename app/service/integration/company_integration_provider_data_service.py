from django.contrib.auth import get_user_model

from app.service.integration.integration_provider_service import (
        IntegrationProviderService,
        INTEGRATION_SERVICE_TYPES,
        INTEGRATION_SERVICE_TYPE_PAYROLL,
        INTEGRATION_PAYROLL_CONNECT_PAYROLL
    )
from app.service.company_personnel_service import CompanyPersonnelService
from app.service.integration.payroll.connect_payroll.connect_payroll_data_service \
import ConnectPayrollDataService

User = get_user_model()


''' This is a facade/orchestration to abstract higher level
    logics from knowing the detailed types of data services
    created for various integration providers 
'''
class CompanyIntegrationProviderDataService(object):

    def __init__(self):
        self.integration_provider_service = IntegrationProviderService()
        self.company_personnel_service = CompanyPersonnelService()

        self._data_service_registry = {}
        for integration_provider_type in INTEGRATION_SERVICE_TYPES:
            self._data_service_registry[integration_provider_type] = {}      

        self._register_data_service_classes()

    def _register_data_service_classes(self):
        # Register all data services
        self._data_service_registry[INTEGRATION_SERVICE_TYPE_PAYROLL][INTEGRATION_PAYROLL_CONNECT_PAYROLL] = ConnectPayrollDataService

    def sync_employee_data_to_remote(self, employee_user_id):
        # Enumerate through all the integration providers associated
        # with the company, identify all registered data services, 
        # and invoke them to sync with the remote
        company_id = self.company_personnel_service.get_company_id_by_employee_user_id(employee_user_id)
        if (not company_id):
            return
        self._enumerate_company_data_services(company_id, lambda data_service: data_service.sync_employee_data_to_remote(employee_user_id))

    def _enumerate_company_data_services(self, company_id, data_service_action):
        # [TODO]: Distributed atomicity is hard to guarantee, when it involves
        #         non-managed number of third-party APIs. 
        #         At least we need to in logging and fault tolerance, and 
        #         monitoring and alerts to follow.  
        company_integration_providers = self.integration_provider_service.get_company_integration_providers(company_id)
        for service_type in company_integration_providers:
            company_service_type_provider = company_integration_providers[service_type]
            if (company_service_type_provider):
                provider_name = company_service_type_provider['integration_provider']['name']
                # Now we have the service type and the provider name, check whether
                # we have a registered data service class
                if (service_type in self._data_service_registry):
                    service_type_data_services = self._data_service_registry[service_type]
                    if (provider_name in service_type_data_services):
                        # create an instance of the date service, and invoke the action
                        data_service = service_type_data_services[provider_name]()
                        data_service_action(data_service)
