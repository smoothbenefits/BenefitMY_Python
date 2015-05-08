from rest_framework import serializers
from app.models.insurance.person_company_supplemental_life_insurance_plan import \
    PersonCompanySupplementalLifeInsurancePlan
from ..hash_pk_serializer_base import HashPkSerializerBase
from company_supplemental_life_insurance_plan_serializer import (
    CompanySupplementalLifeInsurancePlanSerializer,
    CompanySupplementalLifeInsurancePlanPostSerializer)
from ..custom_fields.hash_field import HashField


class PersonCompanySupplementalLifeInsurancePlanSerializer(HashPkSerializerBase):
    company_supplemental_life_insurance_plan = SupplementalLifeInsurancePlanSerializer()
    person = HashField(source="person.id")

    class Meta:
        model = PersonCompanySupplementalLifeInsurancePlan


class PersonCompanySupplementalLifeInsurancePlanPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = PersonCompanySupplementalLifeInsurancePlan
