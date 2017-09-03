from state_tax_election_base import StateTaxElectionBase


class RIStateTaxElection(StateTaxElectionBase):
    
    def __init__(self, is_legal_residence=None, household_name=None):
        super(RIStateTaxElection, self).__init__()

        self.is_legal_residence = is_legal_residence
        self.household_name = household_name
