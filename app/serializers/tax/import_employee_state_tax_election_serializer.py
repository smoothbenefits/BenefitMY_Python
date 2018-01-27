from employee_state_tax_election_serializer import (
    EmployeeStateTaxElectionSerializer,
    EmployeeStateTaxElectionPostSerializer
)
from import_state_tax_election_serializer import ImportStateTaxElectionSerializer


class ImportEmployeeStateTaxElectionSerializer(EmployeeStateTaxElectionSerializer):
    tax_election_data = ImportStateTaxElectionSerializer()
