from rest_framework import serializers
from app.models.aca.employee_1095_c import Employee1095C
from app.serializers.company_serializer import ShallowCompanySerializer
from app.serializers.person_serializer import PersonSimpleSerializer
from ..hash_pk_serializer_base import HashPkSerializerBase

class Employee1095CSerializer(HashPkSerializerBase):
    company = ShallowCompanySerializer()
    person = PersonSimpleSerializer()
    class Meta:
        model = Employee1095C

class Employe1095CPostSerializer(HashPkSerializerBase):
    class Meta:
        model = Employee1095C
