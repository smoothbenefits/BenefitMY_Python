from rest_framework import serializers
from state_tax_election_serializer import StateTaxElectionSerializer
from app.dtos.tax.MA_state_tax_election import MAStateTaxElection


class MAStateTaxElectionSerializer(StateTaxElectionSerializer):
    personal_exemption = serializers.IntegerField(min_value=1, max_value=2)
    spouse_exemption = serializers.IntegerField(min_value=0, max_value=5)
    num_dependents = serializers.IntegerField(min_value=0)
    additional_witholding = serializers.DecimalField(min_value=0.0, decimal_places=2)

    head_of_household = serializers.BooleanField()
    is_blind = serializers.BooleanField()
    is_spouse_blind = serializers.BooleanField()
    is_fulltime_student = serializers.BooleanField()

    def restore_object(self, attrs, instance=None):
        return MAStateTaxElection(**attrs)
