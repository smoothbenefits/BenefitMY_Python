from rest_framework import serializers
from ..custom_fields.hash_field import HashField
from ..hash_pk_serializer_base import HashPkSerializerBase
from app.models.hra.company_hra_plan import CompanyHraPlan
from hra_plan_serializer import HraPlanSerializer

class CompanyHraPlanSerializer(HashPkSerializerBase):
    hra_plan = HraPlanSerializer()
    company = HashField(source="company.id")

    class Meta:
        model = CompanyHraPlan

class CompanyHraPlanPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyHraPlan
