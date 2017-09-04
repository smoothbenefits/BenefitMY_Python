from state_tax_election_base import StateTaxElectionBase


class MAStateTaxElection(StateTaxElectionBase):
    
    def __init__(
        self, personal_exemption=0, spouse_exemption=0, num_dependents=0,
        additional_witholding=0.0, head_of_household=False, is_blind=False,
        is_spouse_blind=False, is_fulltime_student=False):

        super(MAStateTaxElection, self).__init__()

        self.personal_exemption = personal_exemption
        self.spouse_exemption = spouse_exemption
        self.num_dependents = num_dependents
        self.additional_witholding = additional_witholding

        self.head_of_household = head_of_household
        self.is_blind = is_blind
        self.is_spouse_blind = is_spouse_blind
        self.is_fulltime_student = is_fulltime_student

    @property
    def total_exemption(self):
        return self.personal_exemption + self.spouse_exemption + self.num_dependents
