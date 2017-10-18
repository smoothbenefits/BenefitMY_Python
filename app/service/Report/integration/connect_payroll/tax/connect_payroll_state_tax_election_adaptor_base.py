class ConnectPayrollStateTaxElectionAdaptorBase(object):

    ''' @state_tax_election expect a state_tax_election dto
    '''
    def __init__(self, state, state_tax_election):
        self._state = state
        self._state_tax_election = state_tax_election

    def get_filing_status(self):
        raise NotImplementedError()

    def get_total_exemptions(self):
        raise NotImplementedError()

    def get_additional_exemptions(self):
        raise NotImplementedError()

    def get_additional_amount_code(self):
        raise NotImplementedError()

    def get_additional_amount(self):
        raise NotImplementedError()
