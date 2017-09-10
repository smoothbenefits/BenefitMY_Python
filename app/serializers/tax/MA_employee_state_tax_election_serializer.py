from employee_state_tax_election_serializer import (
    EmployeeStateTaxElectionSerializer,
    EmployeeStateTaxElectionPostSerializer
)
from MA_state_tax_election_serializer import MAStateTaxElectionSerializer


class MAEmployeeStateTaxElectionSerializer(EmployeeStateTaxElectionSerializer):
    tax_election_data = MAStateTaxElectionSerializer()


class MAEmployeeStateTaxElectionPostSerializer(EmployeeStateTaxElectionPostSerializer):
    tax_election_data = MAStateTaxElectionSerializer()
