from state_tax_election_base import StateTaxElectionBase


class MAStateTaxElection(StateTaxElectionBase):
    
    def __init__(self, head_of_household=None, allowance=None):
        super(MAStateTaxElection, self).__init__()

        self.head_of_household = head_of_household
        self.allowance = allowance
