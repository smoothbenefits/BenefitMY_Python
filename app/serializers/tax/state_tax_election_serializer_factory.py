from MA_state_tax_election_serializer import MAStateTaxElectionSerializer
from RI_state_tax_election_serializer import RIStateTaxElectionSerializer
from import_state_tax_election_serializer import ImportStateTaxElectionSerializer


''' Factory to provide the proper state tax election serializer (class)
    based on given state.
'''
class StateTaxElectionSerializerFactory(object):
    _state_serializer_map = {
        'MA': MAStateTaxElectionSerializer,
        'RI': RIStateTaxElectionSerializer
    }

    def get_state_tax_election_serializer(self, state, imported=False):
        # For the GET serializer, we need to support the case where consumer
        # is facing a state tax election record that was imported. And here
        # we return the specialized serializer to handle that.
        if (imported):
            return ImportStateTaxElectionSerializer
            
        if (state not in self._state_serializer_map):
            raise ValueError('Given state "{0}" is not supported!'.format(state))
        return self._state_serializer_map[state]
