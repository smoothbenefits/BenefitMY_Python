from app.models.company_features import CompanyFeatures

from custom_fields.hash_field import HashField
from hash_pk_serializer_base import HashPkSerializerBase
from sys_application_feature_serializer import SysApplicationFeatureSerializer


class CompanyFeaturesSerializer(HashPkSerializerBase):

    company_feature = SysApplicationFeatureSerializer()
    company = HashField(source="company.id")

    class Meta:

        model = CompanyFeatures


class CompanyFeaturesPostSerializer(HashPkSerializerBase):

    class Meta:

        model = CompanyFeatures
