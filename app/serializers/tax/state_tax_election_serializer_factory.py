from MA_state_tax_election_serializer import MAStateTaxElectionSerializer
from RI_state_tax_election_serializer import RIStateTaxElectionSerializer


class StateTaxElectionSerializerFactory(object):
    _state_serializer_map = {
        'MA': MAStateTaxElectionSerializer,
        'RI': RIStateTaxElectionSerializer
    }

    def get_state_tax_election_serializer(self, state):
        if (state not in self._state_serializer_map):
            raise ValueError('Given state "{0}" is not supported!'.format(state))
        return self._state_serializer_map[state]
