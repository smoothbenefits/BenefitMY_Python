from rest_framework import serializers
from app.models.company import Company

from person_serializer import (
    PersonSerializer,
    PersonPostSerializer)


from address_serializer import AddressSerializer


class CompanySerializer(serializers.ModelSerializer):

    addresses = AddressSerializer(many=True)
    contacts = PersonSerializer(many=True)

    class Meta:

        model = Company
        fields = ('id',
                  'name',
                  'contacts',
                  'addresses')
        depth = 1


class CompanyPostSerializer(serializers.ModelSerializer):

    addresses = AddressSerializer(many=True, allow_add_remove=True)
    contacts = PersonPostSerializer(many=True, allow_add_remove=True)

    class Meta:

        model = Company
        fields = ('name',
                  'contacts',
                  'addresses')
