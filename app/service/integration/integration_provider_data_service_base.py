from django.contrib.auth import get_user_model

from app.service.integration.integration_provider_service import \
    IntegrationProviderService

User = get_user_model()


class IntegrationProviderDataServiceBase(object):

    def __init__(self):
        self._integration_provider_service = IntegrationProviderService()

    def sync_employee_data_to_remote(self, employee_user_id):
        pass

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
