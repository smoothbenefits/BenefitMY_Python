from rest_framework import serializers
from ..custom_fields.hash_field import HashField
from ..hash_pk_serializer_base import HashPkSerializerBase
from ..sys_suppl_life_insurance_condition_serializer import \
    SysSupplLifeInsuranceConditionSerializer
from app.models.insurance.person_comp_suppl_life_insurance_plan import \
    PersonCompSupplLifeInsurancePlan
from company_supplemental_life_insurance_plan_serializer import (
    CompanySupplementalLifeInsurancePlanSerializer,
    CompanySupplementalLifeInsurancePlanPostSerializer)


class PersonCompanySupplementalLifeInsurancePlanSerializer(HashPkSerializerBase):
    company_supplemental_life_insurance_plan = CompanySupplementalLifeInsurancePlanSerializer()
    self_condition = SysSupplLifeInsuranceConditionSerializer()
    spouse_condition = SysSupplLifeInsuranceConditionSerializer()
    person = HashField(source="person.id")

    class Meta:
        model = PersonCompSupplLifeInsurancePlan


class PersonCompanySupplementalLifeInsurancePlanPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = PersonCompSupplLifeInsurancePlan
