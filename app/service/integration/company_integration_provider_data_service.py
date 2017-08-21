import traceback
from django.contrib.auth import get_user_model

from app.service.integration.integration_provider_service import (
        IntegrationProviderService,
        INTEGRATION_SERVICE_TYPES,
        INTEGRATION_SERVICE_TYPE_PAYROLL,
        INTEGRATION_PAYROLL_CONNECT_PAYROLL,
        INTEGRATION_PAYROLL_ADVANTAGE_PAYROLL
    )
from app.service.company_personnel_service import CompanyPersonnelService
from app.service.integration.payroll.connect_payroll.connect_payroll_data_service \
import ConnectPayrollDataService
from app.service.integration.payroll.advantage_payroll.advantage_payroll_data_service \
import AdvantagePayrollDataService
from app.service.monitoring.logging_service import LoggingService

User = get_user_model()


''' This is a facade/orchestration to abstract higher level
    logics from knowing the detailed types of data services
    created for various integration providers 
'''
class CompanyIntegrationProviderDataService(object):
    _logger = LoggingService()

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
        self._data_service_registry[INTEGRATION_SERVICE_TYPE_PAYROLL][INTEGRATION_PAYROLL_ADVANTAGE_PAYROLL] = AdvantagePayrollDataService

    def sync_employee_data_to_remote(self, employee_user_id):
        # Enumerate through all the integration providers associated
        # with the company, identify all registered data services, 
        # and invoke them to sync with the remote
        company_id = self.company_personnel_service.get_company_id_by_employee_user_id(employee_user_id)
        if (not company_id):
            return
        return self._enumerate_company_data_services(company_id, lambda data_service: data_service.sync_employee_data_to_remote(employee_user_id))

    def generate_and_record_external_employee_number(self, employee_user_id):
        company_id = self.company_personnel_service.get_company_id_by_employee_user_id(employee_user_id)
        if (not company_id):
            raise ValueError('The given employee user ID "{0}" is not properly linked to a valid company.'.format(employee_user_id))
        return self._enumerate_company_data_services(company_id, lambda data_service: data_service.generate_and_record_external_employee_number(employee_user_id))

    def _enumerate_company_data_services(self, company_id, data_service_action):
        # Record failed actions and report back to caller
        failed_data_service_records = []

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

                        # Collect the current data service specs into a record instance
                        # for logging and anormaly reporting to upstream
                        service_action_record = IntegrationDataServiceActionRecord(
                            company_id=company_id,
                            service_type=service_type,
                            provider_name=provider_name,
                            service_action=data_service_action
                        )

                        try:
                            data_service_action(data_service)
                            self._logger.error('Successfully executed integration data action')
                            self._logger.info(service_action_record)
                        except Exception as e:
                            self._logger.error('Failed to complete integration data action')
                            self._logger.info(service_action_record)
                            failed_data_service_records.append(service_action_record)
                else:
                    self._logger.warning('Unsupported integration service type encoutered: "{0}"'.format(service_type))

        return failed_data_service_records


''' A data object to hold specs involved in a single integrtion data service
    This is more for reporting purposes
'''
class IntegrationDataServiceActionRecord(object):
    def __init__(self, company_id, service_type, provider_name, service_action):
        self.company_id = company_id
        self.service_type = service_type
        self.provider_name = provider_name
        self.service_action = service_action
