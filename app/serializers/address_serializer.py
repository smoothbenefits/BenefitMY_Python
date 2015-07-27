from rest_framework import serializers
from app.models.address import Address
from hash_pk_serializer_base import HashPkSerializerBase


class AddressSerializer(HashPkSerializerBase):

    class Meta:
        model = Address
        fields = ('id',
                  'address_type',
                  'street_1',
                  'street_2',
                  'city',
                  'state',
                  'zipcode')
