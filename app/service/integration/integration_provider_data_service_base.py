from django.contrib.auth import get_user_model

from app.models.company_user import (
    CompanyUser,
    USER_TYPE_EMPLOYEE
)
from app.models.integration.company_user_integration_provider import CompanyUserIntegrationProvider
from app.models.integration.integration_provider import IntegrationProvider

User = get_user_model()


class IntegrationProviderDataServiceBase(object):

    def __init__(self):
        pass

    def sync_employee_data_to_remote(self, employee_user_id):
        pass

    def _get_employee_external_id(self, employee_user_id, service_type, provider_name):
        company_user_integration_provider = self.__get_employee_integration_provider_model(
                employee_user_id,
                service_type,
                provider_name
            )
        if (company_user_integration_provider):
            return company_user_integration_provider.company_user_external_id
        return None

    def _set_employee_external_id(self, employee_user_id, service_type, provider_name, external_id):
        company_user_integration_provider = self.__get_employee_integration_provider_model(
                employee_user_id,
                service_type,
                provider_name
            )
        if (company_user_integration_provider):
            # update the existing record
            company_user_integration_provider.company_user_external_id = external_id
            company_user_integration_provider.save()
        else:
            # create a new record
            company_user = self.__get_company_user_model(employee_user_id)
            integration_provider = self.__get_integration_provider_model(service_type, provider_name)
            CompanyUserIntegrationProvider.objects.create(
                company_user=company_user,
                integration_provider=integration_provider,
                company_user_external_id=external_id)

    def __get_employee_integration_provider_model(self, employee_user_id, service_type, provider_name):
        company_user_integration_providers = CompanyUserIntegrationProvider.objects.filter(
            company_user__user=employee_user_id,
            integration_provider__service_type=service_type,
            integration_provider__name=provider_name)
        if (len(company_user_integration_providers)):
            return company_user_integration_providers[0]
        return None

    def __get_integration_provider_model(self, service_type, provider_name):
        return IntegrationProvider.objects.get(
            service_type=service_type,
            name=provider_name)

    def __get_company_user_model(self, employee_user_id):
        return CompanyUser.objects.get(
            user=employee_user_id,
            company_user_type=USER_TYPE_EMPLOYEE
        )
