from rest_framework import serializers
from state_tax_election_serializer import StateTaxElectionSerializer
from app.dtos.tax.import_state_tax_election import ImportStateTaxElection


class ImportStateTaxElectionSerializer(StateTaxElectionSerializer):
    allowance = serializers.IntegerField(min_value=0)
    filing_status = serializers.CharField(min_length=1, max_length=1)
    extra_amount = serializers.DecimalField(min_value=0.0, decimal_places=2)

    def restore_object(self, attrs, instance=None):
        return ImportStateTaxElection(**attrs)
