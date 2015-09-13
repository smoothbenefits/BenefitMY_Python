from rest_framework import serializers
from app.models.company import Company

from person_serializer import (
    PersonSerializer,
    PersonPostSerializer)

from sys_period_definition_serializer import SysPeriodDefinitionSerializer
from address_serializer import AddressSerializer
from hash_pk_serializer_base import HashPkSerializerBase

class ShallowCompanySerializer(HashPkSerializerBase):
  pay_period_definition = SysPeriodDefinitionSerializer()
  class Meta:

        model = Company
        fields = ('id',
                  'name',
                  'pay_period_definition',
                  'ein',
                  'offer_of_coverage_code')

class CompanySerializer(HashPkSerializerBase):

    addresses = AddressSerializer(many=True)
    contacts = PersonSerializer(many=True)
    pay_period_definition = SysPeriodDefinitionSerializer()

    class Meta:

        model = Company
        fields = ('id',
                  'name',
                  'pay_period_definition',
                  'contacts',
                  'addresses',
                  'ein',
                  'offer_of_coverage_code')

class CompanyPostSerializer(HashPkSerializerBase):

    addresses = AddressSerializer(many=True, allow_add_remove=True)
    contacts = PersonPostSerializer(many=True, allow_add_remove=True)

    class Meta:

        model = Company
        fields = ('id',
                  'name',
                  'pay_period_definition',
                  'contacts',
                  'addresses',
                  'ein',
                  'offer_of_coverage_code')
