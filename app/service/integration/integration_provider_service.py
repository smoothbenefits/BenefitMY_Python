from django.conf import settings
from django.contrib.auth import get_user_model

from app.models.integration.integration_provider import (
    IntegrationProvider,
    INTEGRATION_SERVICE_TYPES,
    INTEGRATION_SERVICE_TYPE_PAYROLL
)
from app.models.integration.company_integration_provider import \
    CompanyIntegrationProvider 
from app.models.integration.company_user_integration_provider import \
    CompanyUserIntegrationProvider
from app.models.company_user import (
    CompanyUser,
    USER_TYPE_EMPLOYEE
)
from app.serializers.integration.company_integration_provider_serializer import \
    CompanyIntegrationProviderSerializer

User = get_user_model()

# Payroll service provider names
INTEGRATION_PAYROLL_ADVANTAGE_PAYROLL = 'Advantage Payroll'
INTEGRATION_PAYROLL_CONNECT_PAYROLL = 'Connect Payroll'


class IntegrationProviderService(object):

    def get_company_integration_providers(self, company_id):
        result = {}

        company_providers = CompanyIntegrationProvider.objects.filter(company_id=company_id)
        
        for service_type in INTEGRATION_SERVICE_TYPES:
            result[service_type] = None

        for company_provider in company_providers:
            serialized = CompanyIntegrationProviderSerializer(company_provider)
            result[company_provider.integration_provider.service_type] = serialized.data

        return result

    def get_company_integration_provider_external_id(self, company_id, service_type, provider_name):
        company_integration_providers = self.get_company_integration_providers(company_id)
        integration_provider = company_integration_providers[service_type]
        if (not integration_provider):
            return None
        company_provider_name = integration_provider['integration_provider']['name']
        if (company_provider_name != provider_name):
            return None
        return integration_provider['company_external_id']

    def get_employee_integration_provider_external_id(self, employee_user_id, service_type, provider_name):
        company_user_integration_provider = self._get_employee_integration_provider_model(
                employee_user_id,
                service_type,
                provider_name
            )
        if (company_user_integration_provider):
            return company_user_integration_provider.company_user_external_id
        return None

    def set_employee_integration_provider_external_id(self, employee_user_id, service_type, provider_name, external_id):
        company_user_integration_provider = self._get_employee_integration_provider_model(
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
            company_user = self._get_company_user_model(employee_user_id)
            integration_provider = self._get_integration_provider_model(service_type, provider_name)
            CompanyUserIntegrationProvider.objects.create(
                company_user=company_user,
                integration_provider=integration_provider,
                company_user_external_id=external_id)

    def _get_employee_integration_provider_model(self, employee_user_id, service_type, provider_name):
        try:
            return CompanyUserIntegrationProvider.objects.get(
                company_user__user=employee_user_id,
                integration_provider__service_type=service_type,
                integration_provider__name=provider_name)
        except CompanyUserIntegrationProvider.DoesNotExist:
            return None

    def _get_company_user_model(self, employee_user_id):
        return CompanyUser.objects.get(
            user=employee_user_id,
            company_user_type=USER_TYPE_EMPLOYEE
        )

    def _get_integration_provider_model(self, service_type, provider_name):
        return IntegrationProvider.objects.get(
            service_type=service_type,
            name=provider_name)
