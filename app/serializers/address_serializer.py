from rest_framework import serializers
from app.models.address import Address


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ('id',
                  'address_type',
                  'street_1',
                  'street_2',
                  'city',
                  'state',
                  'zipcode')

