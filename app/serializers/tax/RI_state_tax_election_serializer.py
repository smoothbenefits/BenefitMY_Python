from rest_framework import serializers
from state_tax_election_serializer import StateTaxElectionSerializer
from app.dtos.tax.RI_state_tax_election import RIStateTaxElection


class RIStateTaxElectionSerializer(StateTaxElectionSerializer):
    is_not_dependent = serializers.BooleanField()
    spouse_is_dependent = serializers.BooleanField()
    num_dependents = serializers.IntegerField(min_value=0)
    additional_allowances = serializers.IntegerField(min_value=0)

    additional_witholding = serializers.DecimalField(min_value=0.0, decimal_places=2)
    is_exempt_status = serializers.BooleanField()
    is_exempt_ms_status = serializers.BooleanField()

    def restore_object(self, attrs, instance=None):
        return RIStateTaxElection(**attrs)
