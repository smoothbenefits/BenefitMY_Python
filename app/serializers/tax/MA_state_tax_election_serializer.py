from rest_framework import serializers
from state_tax_election_serializer import StateTaxElectionSerializer
from app.dtos.tax.MA_state_tax_election import MAStateTaxElection


class MAStateTaxElectionSerializer(StateTaxElectionSerializer):
    head_of_household = serializers.BooleanField(default=False)
    allowance = serializers.IntegerField(min_value=0)

    def restore_object(self, attrs, instance=None):
        return MAStateTaxElection(**attrs)
