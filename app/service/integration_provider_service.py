from django.conf import settings
from django.contrib.auth import get_user_model

from app.models.integration.integration_provider import (
    IntegrationProvider,
    INTEGRATION_SERVICE_TYPES
)
from app.models.integration.company_integration_provider import \
    CompanyIntegrationProvider 
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
