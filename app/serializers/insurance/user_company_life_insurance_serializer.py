from rest_framework import serializers

from app.models.insurance.user_company_life_insurance_plan import \
    UserCompanyLifeInsurancePlan

from life_insurance_beneficiary_serializer import \
    (LifeInsuranceBeneficiarySerializer, LifeInsuranceBeneficiaryPostSerializer)

from company_life_insurance_plan_serializer import CompanyLifeInsurancePlanSerializer

from ..hash_pk_serializer_base import HashPkSerializerBase
from ..custom_fields.hash_field import HashField

class UserCompanyLifeInsuranceSerializer(HashPkSerializerBase):
    life_insurance_beneficiary = LifeInsuranceBeneficiarySerializer(many=True)
    user = HashField(source="user.id")
    company_life_insurance = CompanyLifeInsurancePlanSerializer()
    person = HashField(source="person.id")

    class Meta:
        model = UserCompanyLifeInsurancePlan


class UserCompanyLifeInsurancePostSerializer(serializers.ModelSerializer):
    life_insurance_beneficiary = LifeInsuranceBeneficiaryPostSerializer(many=True,allow_add_remove=True)

    class Meta:
        model = UserCompanyLifeInsurancePlan