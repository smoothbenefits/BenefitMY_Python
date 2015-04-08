from app.models.company_features import CompanyFeatures

from hash_pk_serializer_base import HashPkSerializerBase


class CompanyFeaturesSerializer(HashPkSerializerBase):

    class Meta:

        model = CompanyFeatures
