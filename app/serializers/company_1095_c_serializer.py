from rest_framework import serializers
from app.models.company_1095_c import Company1095C
from app.serializers.company_serializer import ShallowCompanySerializer
from hash_pk_serializer_base import HashPkSerializerBase



class Company1095CSerializer(HashPkSerializerBase):
    company = ShallowCompanySerializer()
    class Meta:
        model = Company1095C

class Company1095CPostSerializer(HashPkSerializerBase):
    class Meta:
        model = Company1095C
