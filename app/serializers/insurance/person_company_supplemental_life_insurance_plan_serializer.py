from rest_framework import serializers
from app.models.insurance.person_comp_suppl_life_insurance_plan import \
    PersonCompSupplLifeInsurancePlan
from ..hash_pk_serializer_base import HashPkSerializerBase
from company_supplemental_life_insurance_plan_serializer import (
    CompanySupplementalLifeInsurancePlanSerializer,
    CompanySupplementalLifeInsurancePlanPostSerializer)
from ..custom_fields.hash_field import HashField


class PersonCompanySupplementalLifeInsurancePlanSerializer(HashPkSerializerBase):
    company_supplemental_life_insurance_plan = CompanySupplementalLifeInsurancePlanSerializer()
    person = HashField(source="person.id")

    class Meta:
        model = PersonCompSupplLifeInsurancePlan


class PersonCompanySupplementalLifeInsurancePlanPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = PersonCompSupplLifeInsurancePlan
