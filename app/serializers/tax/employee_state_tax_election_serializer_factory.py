from MA_employee_state_tax_election_serializer import (
    MAEmployeeStateTaxElectionSerializer,
    MAEmployeeStateTaxElectionPostSerializer,
)
from RI_employee_state_tax_election_serializer import (
    RIEmployeeStateTaxElectionSerializer,
    RIEmployeeStateTaxElectionPostSerializer,
)


''' Factory to provide the proper employee state tax election serializer (class)
    based on given state.
'''
class EmployeeStateTaxElectionSerializerFactory(object):
    _employee_state_serializer_map = {
        'MA': MAEmployeeStateTaxElectionSerializer,
        'RI': RIEmployeeStateTaxElectionSerializer
    }

    _employee_state_post_serializer_map = {
        'MA': MAEmployeeStateTaxElectionPostSerializer,
        'RI': RIEmployeeStateTaxElectionPostSerializer
    }

    def get_employee_state_tax_election_serializer(self, state):
        if (state not in self._employee_state_serializer_map):
            raise ValueError('Given state "{0}" is not supported!'.format(state))
        return self._employee_state_serializer_map[state]

    def get_employee_state_tax_election_post_serializer(self, state):
        if (state not in self._employee_state_post_serializer_map):
            raise ValueError('Given state "{0}" is not supported!'.format(state))
        return self._employee_state_post_serializer_map[state]
