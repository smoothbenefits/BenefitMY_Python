from rest_framework import serializers
from ..custom_fields.hash_field import HashField
from ..hash_pk_serializer_base import HashPkSerializerBase
from app.models.insurance.company_ltd_age_based_rate import CompanyLtdAgeBasedRate

class CompanyLtdAgeBasedRateSerializer(HashPkSerializerBase):

    company_ltd_insurance_plan = HashField(source="company_ltd_insurance_plan.id")

    class Meta:
        model = CompanyLtdAgeBasedRate


class CompanyLtdAgeBasedRatePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyLtdAgeBasedRate
