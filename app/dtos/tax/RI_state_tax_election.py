from state_tax_election_base import StateTaxElectionBase


class RIStateTaxElection(StateTaxElectionBase):
    
    def __init__(
        self, is_not_dependent=False, spouse_is_dependent=False, num_dependents=0,
        additional_allowances=0, additional_witholding=0.0, is_exempt_status=False,
        is_exempt_ms_status=False):
        super(RIStateTaxElection, self).__init__()

        self.is_not_dependent = is_not_dependent
        self.spouse_is_dependent = spouse_is_dependent
        self.num_dependents = num_dependents
        self.additional_allowances = additional_allowances

        self.additional_witholding = additional_witholding
        self.is_exempt_status = is_exempt_status
        self.is_exempt_ms_status = is_exempt_ms_status

        if (self.is_exempt_status and self.is_exempt_ms_status):
            raise ValueError('Invalid to have both EXEMPT and EXEMPT-MS status')

    @property
    def total_exemption(self):
        total = 0
        if (self.is_not_dependent):
            total = total + 1
        if (self.spouse_is_dependent):
            total = total + 1
        total = total + self.num_dependents
        total = total + self.additional_allowances

        if (total >= 10):
            return 10

        return total

    @property
    def exempt_status(self):
        if (self.is_exempt_status):
            return 'EXEMPT'
        if (self.is_exempt_ms_status):
            return 'EXEMPT-MS'
