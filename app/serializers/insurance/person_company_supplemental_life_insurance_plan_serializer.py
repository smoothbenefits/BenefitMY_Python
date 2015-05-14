from rest_framework import serializers
from ..custom_fields.hash_field import HashField
from ..hash_pk_serializer_base import HashPkSerializerBase
from ..sys_suppl_life_insurance_condition_serializer import \
    SysSupplLifeInsuranceConditionSerializer
from app.models.insurance.person_comp_suppl_life_insurance_plan import \
    PersonCompSupplLifeInsurancePlan
from supplemental_life_insurance_beneficiary_serializer import (
    SupplementalLifeInsuranceBeneficiarySerializer,
    SupplementalLifeInsuranceBeneficiaryPostSerializer)
from company_supplemental_life_insurance_plan_serializer import (
    CompanySupplementalLifeInsurancePlanSerializer,
    CompanySupplementalLifeInsurancePlanPostSerializer)


class PersonCompanySupplementalLifeInsurancePlanSerializer(HashPkSerializerBase):
    company_supplemental_life_insurance_plan = CompanySupplementalLifeInsurancePlanSerializer()
    suppl_life_insurance_beneficiary = SupplementalLifeInsuranceBeneficiarySerializer(many=True)
    self_condition = SysSupplLifeInsuranceConditionSerializer()
    spouse_condition = SysSupplLifeInsuranceConditionSerializer()
    person = HashField(source="person.id")

    class Meta:
        model = PersonCompSupplLifeInsurancePlan


class PersonCompanySupplementalLifeInsurancePlanPostSerializer(serializers.ModelSerializer):
    suppl_life_insurance_beneficiary = SupplementalLifeInsuranceBeneficiaryPostSerializer(many=True, allow_add_remove=True)

    class Meta:
        model = PersonCompSupplLifeInsurancePlan
