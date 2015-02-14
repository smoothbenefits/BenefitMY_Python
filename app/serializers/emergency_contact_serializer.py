from rest_framework import serializers
from app.models.emergency_contact import EmergencyContact
from hash_pk_serializer_base import HashPkSerializerBase


class EmergencyContactSerializer(HashPkSerializerBase):

    class Meta:
        model = EmergencyContact
