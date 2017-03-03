from app.models.integration.company_integration_provider import CompanyIntegrationProvider
from ..custom_fields.hash_field import HashField
from ..hash_pk_serializer_base import HashPkSerializerBase
from integration_provider_serializer import IntegrationProviderSerializer


class CompanyIntegrationProviderSerializer(HashPkSerializerBase):
    company = HashField(source="company.id")
    integration_provider = IntegrationProviderSerializer()

    class Meta:
        model = CompanyIntegrationProvider
