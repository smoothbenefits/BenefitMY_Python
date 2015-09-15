from rest_framework import serializers
from ..custom_fields.hash_field import HashField
from ..hash_pk_serializer_base import HashPkSerializerBase
from app.models.insurance.company_std_age_based_rate import CompanyStdAgeBasedRate

class CompanyStdAgeBasedRateSerializer(HashPkSerializerBase):

    company_std_insurance_plan = HashField(source="company_std_insurance_plan.id")

    class Meta:
        model = CompanyStdAgeBasedRate


class CompanyStdAgeBasedRatePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyStdAgeBasedRate
