from . import FieldWithIdOrObject
from rest_framework import serializers
from custom_fields.hash_field import HashField
from hash_pk_serializer_base import HashPkSerializerBase

from app.models.company_division import CompanyDivision


class CompanyDivisionSerializer(HashPkSerializerBase):
    company = HashField(source="company.id")

    class Meta:
        model = CompanyDivision


class CompanyDivisionPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyDivision

class CompanyDivisionFieldWithId(FieldWithIdOrObject):
    model = CompanyDivision
    serializer = CompanyDivisionSerializer
