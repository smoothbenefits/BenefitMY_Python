import json
from rest_framework import serializers
from app.models.tax.employee_state_tax_election import EmployeeStateTaxElection
from ..hash_pk_serializer_base import HashPkSerializerBase
from ..custom_fields.hash_field import HashField


class EmployeeStateTaxElectionSerializer(HashPkSerializerBase):
    user = HashField(source="user.id")

    # Needs to override this
    tax_election_data = None

    class Meta:
        model = EmployeeStateTaxElection
        exclude = ('id', 'data')


class EmployeeStateTaxElectionPostSerializer(HashPkSerializerBase):
    # Needs to override this
    tax_election_data = None
    
    class Meta:
        model = EmployeeStateTaxElection
        exclude = ('id', 'data')
