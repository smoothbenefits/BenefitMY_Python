from app.models.company_user_features import CompanyUserFeatures
from hash_pk_serializer_base import HashPkSerializerBase
from sys_application_feature_serializer import SysApplicationFeatureSerializer


class CompanyUserFeaturesSerializer(HashPkSerializerBase):
    feature = SysApplicationFeatureSerializer()
    company_user = HashField(source="company_user.id")

    class Meta:
        model = CompanyUserFeatures
