from app.models.integration.integration_provider import IntegrationProvider
from ..hash_pk_serializer_base import HashPkSerializerBase


class IntegrationProviderSerializer(HashPkSerializerBase):

    class Meta:
        model = IntegrationProvider
