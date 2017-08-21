from django.contrib.auth import get_user_model

from app.service.integration.integration_provider_service import \
    IntegrationProviderService

User = get_user_model()


class IntegrationProviderDataServiceBase(object):

    def __init__(self):
        self._integration_provider_service = IntegrationProviderService()

    #############################################
    ## Abstract members
    #############################################

    def _integration_service_type(self):
        raise NotImplementedError('Concrete implementation needs to specify the integration service type it supports.')  

    def _integration_provider_name(self):
        raise NotImplementedError('Concrete implementation needs to specify the name of the service provider it supports.') 

    def _internal_sync_employee_data_to_remote(self, employee_user_id):
        pass

    def _internal_generate_and_record_external_employee_number(self, employee_user_id):
        pass

    #############################################
    ## Abstract members
    #############################################

    ''' Whether this given employee is supported by this integration service data facility
        i.e. whether the corresponding integration service type and provider is available
        to the given employee
    '''
    def is_supported(self, employee_user_id):
        return self._integration_provider_service.is_integration_service_available_to_employee(
            employee_user_id,
            self._integration_service_type(),
            self._integration_provider_name())

    ''' Synchronize all appropriate data related to the given
        employee to the external service provider
    '''
    def sync_employee_data_to_remote(self, employee_user_id):
        if (not self.is_supported(employee_user_id)):
            raise ValueError('The operation is not supported for employee: "{0}"'.format(employee_user_id))
        self._internal_sync_employee_data_to_remote(employee_user_id)

    ''' Generate external employee number (normally for a new employee),
        and record that in WBM system.
    ''' 
    def generate_and_record_external_employee_number(self, employee_user_id):
        if (not self.is_supported(employee_user_id)):
            raise ValueError('The operation is not supported for employee: "{0}"'.format(employee_user_id))
        self._internal_generate_and_record_external_employee_number(employee_user_id)

    def _get_employee_external_id(self, employee_user_id, service_type, provider_name):
        return self._integration_provider_service.get_employee_integration_provider_external_id(
            employee_user_id,
            service_type,
            provider_name)

    def _set_employee_external_id(self, employee_user_id, service_type, provider_name, external_id):
        self._integration_provider_service.set_employee_integration_provider_external_id(
            employee_user_id,
            service_type,
            provider_name,
            external_id)
