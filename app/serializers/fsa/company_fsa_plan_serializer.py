from rest_framework import serializers
from app.models.fsa.company_fsa_plan import CompanyFsaPlan
from fsa_serializer import (
    FsaSerializer,
    FsaPostSerializer)
from ..custom_fields.hash_field import HashField
from ..hash_pk_serializer_base import HashPkSerializerBase


class CompanyFsaPlanSerializer(HashPkSerializerBase):
    fsa_plan = FsaSerializer()
    company = HashField(source="company.id")

    class Meta:
        model = CompanyFsaPlan

class CompanyFsaPlanPostSerializer(serializers.ModelSerializer):
    fsa_plan = FsaPostSerializer()

    class Meta:
        model = CompanyFsaPlan
