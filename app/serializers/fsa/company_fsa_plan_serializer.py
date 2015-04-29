from rest_framework import serializers
from app.models.fsa.fsa import CompanyFsaPlan
from fsa_serializer import (
    FsaSerializer,
    FsaPostSerializer)
from ..custom_fields.hash_field import HashField
from ..hash_pk_serializer_base import HashPkSerializerBase


class CompanyFsaPlanSerializer(HashPkSerializerBase):
    fsa_plan = LtdInsurancePlanSerializer()
    company = HashField(source="company.id")

    class Meta:
        model = CompanyFsaPlan


class CompanyFsaPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyFsaPlan
