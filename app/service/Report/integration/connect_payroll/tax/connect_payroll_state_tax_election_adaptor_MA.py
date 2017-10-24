from .connect_payroll_state_tax_election_adaptor_base import ConnectPayrollStateTaxElectionAdaptorBase


class ConnectPayrollStateTaxElectionAdaptorMA(ConnectPayrollStateTaxElectionAdaptorBase):

    def __init__(self, state, state_tax_election):
        super(ConnectPayrollStateTaxElectionAdaptorMA, self).__init__(state, state_tax_election)

    def get_filing_status(self):
        return 'MA'

    def get_total_exemptions(self):
        return '10'

    def get_additional_exemptions(self):
        return '2'

    def get_additional_amount_code(self):
        return 'A'

    def get_additional_amount(self):
        return 0.22
