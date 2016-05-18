from rest_framework import serializers
from ..custom_fields.hash_field import HashField
from ..hash_pk_serializer_base import HashPkSerializerBase

from app.models.workers_comp.employee_phraseology import \
    EmployeePhraseology
from phraseology_serializer import PhraseologySerializer


class EmployeePhraseologySerializer(HashPkSerializerBase):
    phraseology = PhraseologySerializer()
    employee_person = HashField(source="employee_person.id")
    is_active = serializers.Field(source="is_active")

    class Meta:
        model = EmployeePhraseology


class EmployeePhraseologyPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmployeePhraseology
