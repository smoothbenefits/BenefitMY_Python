from employee_state_tax_election_serializer import (
    EmployeeStateTaxElectionSerializer,
    EmployeeStateTaxElectionPostSerializer
)
from RI_state_tax_election_serializer import RIStateTaxElectionSerializer


class RIEmployeeStateTaxElectionSerializer(EmployeeStateTaxElectionSerializer):
    tax_election_data = RIStateTaxElectionSerializer()


class RIEmployeeStateTaxElectionPostSerializer(EmployeeStateTaxElectionPostSerializer):
    tax_election_data = RIStateTaxElectionSerializer()
