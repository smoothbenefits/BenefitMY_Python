from rest_framework import serializers
from app.models.fsa.company_fsa_plan import CompanyFsaPlan
from fsa_plan_serializer import FsaPlanSerializer
from ..company_serializer import ShallowCompanySerializer
from ..custom_fields.hash_field import HashField
from ..hash_pk_serializer_base import HashPkSerializerBase


class CompanyFsaPlanSerializer(HashPkSerializerBase):
    fsa_plan = FsaPlanSerializer()
    company = ShallowCompanySerializer()

    class Meta:
        model = CompanyFsaPlan

class CompanyFsaPlanPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyFsaPlan
