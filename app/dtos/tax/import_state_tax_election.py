from state_tax_election_base import (
    StateTaxElectionBase,
    STATE_TAX_DATA_SOURCE_IMPORT
)


class ImportStateTaxElection(StateTaxElectionBase):
    
    def __init__(
        self, filing_status, allowance=0, extra_amount=0.0):

        super(ImportStateTaxElection, self).__init__()

        self.allowance = allowance
        self.filing_status = filing_status
        self.extra_amount = extra_amount

    @property
    def data_source(self):
        return STATE_TAX_DATA_SOURCE_IMPORT
