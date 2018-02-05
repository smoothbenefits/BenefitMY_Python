from .connect_payroll_state_tax_election_adaptor_base import ConnectPayrollStateTaxElectionAdaptorBase


class ConnectPayrollStateTaxElectionAdaptorImport(ConnectPayrollStateTaxElectionAdaptorBase):

    def __init__(self, state, state_tax_election):
        super(ConnectPayrollStateTaxElectionAdaptorImport, self).__init__(state, state_tax_election)
        self.election_data = state_tax_election

    def get_filing_status(self):
        return self.election_data.filing_status

    def get_total_exemptions(self):
        return self.election_data.allowance

    def get_additional_exemptions(self):
        return None

    def get_additional_amount_code(self):
        return 'A'

    def get_additional_amount(self):
        return self.election_data.extra_amount
