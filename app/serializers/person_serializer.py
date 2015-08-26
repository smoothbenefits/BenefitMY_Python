from rest_framework import serializers
from app.models.person import Person

from phone_serializer import PhoneSerializer
from address_serializer import AddressSerializer
from emergency_contact_serializer import EmergencyContactSerializer
from hash_pk_serializer_base import HashPkSerializerBase
from custom_fields.hash_field import HashField


class PersonSimpleSerializer(HashPkSerializerBase):
  class Meta:
    model=Person


class PersonSerializer(HashPkSerializerBase):

    addresses = AddressSerializer(many=True)
    phones = PhoneSerializer(many=True)
    emergency_contact = EmergencyContactSerializer(many=True)
    company = HashField(source="company.id")
    user = HashField(source="user.id")

    class Meta:

        model = Person
        fields = ('id',
                  'person_type',
                  'reason_for_change',
                  'relationship',
                  'first_name',
                  'last_name',
                  'middle_name',
                  'ssn',
                  'email',
                  'birth_date',
                  'phones',
                  'addresses',
                  'company',
                  'user',
                  'emergency_contact',
                  'gender')


class PersonFullPostSerializer(HashPkSerializerBase):

    addresses = AddressSerializer(many=True, allow_add_remove=True)
    phones = PhoneSerializer(many=True, allow_add_remove=True)
    emergency_contact = EmergencyContactSerializer(
        many=True,
        allow_add_remove=True)

    class Meta:

        model = Person
        fields = ('id',
                  'person_type',
                  'reason_for_change',
                  'relationship',
                  'first_name',
                  'last_name',
                  'middle_name',
                  'ssn',
                  'email',
                  'birth_date',
                  'phones',
                  'addresses',
                  'company',
                  'user',
                  'emergency_contact',
                  'gender')


class PersonPostSerializer(HashPkSerializerBase):

    phones = PhoneSerializer(many=True, allow_add_remove=True)

    class Meta:

        model = Person
        fields = ('person_type',
                  'first_name',
                  'middle_name',
                  'last_name',
                  'email',
                  'phones',
                  'relationship',
                  'reason_for_change',
                  'user',
                  'gender')
