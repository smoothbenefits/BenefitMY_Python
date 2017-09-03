from rest_framework import serializers
from state_tax_election_serializer import StateTaxElectionSerializer
from app.dtos.tax.RI_state_tax_election import RIStateTaxElection


class RIStateTaxElectionSerializer(StateTaxElectionSerializer):
    is_legal_residence = serializers.BooleanField(default=False)
    household_name = serializers.CharField(max_length=255)

    def restore_object(self, attrs, instance=None):
        return RIStateTaxElection(**attrs)
