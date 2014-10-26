from rest_framework import serializers
from app.models.person import Person

from phone_serializer import PhoneSerializer
from address_serializer import AddressSerializer

class PersonSerializer(serializers.ModelSerializer):

    addresses = AddressSerializer(many=True)
    phones = PhoneSerializer(many=True)
    class Meta:

        model = Person
        fields = ('id',
                  'person_type',
                  'relationship',
                  'ssn',
                  'full_name',
                  'email',
                  'phones',
                  'addresses',
                  'company',
                  'user')

class PersonPostSerializer(serializers.ModelSerializer):

    phones = PhoneSerializer(many=True)

    class Meta:

        model = Person
        fields = ('person_type',
                  'full_name',
                  'email',
                  'phones')

