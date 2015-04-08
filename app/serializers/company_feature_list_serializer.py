from app.models.company_feature_list import CompanyFeatureList

from hash_pk_serializer_base import HashPkSerializerBase


class CompanyFeatureListSerializer(HashPkSerializerBase):

    class Meta:
        model = CompanyFeatureList
