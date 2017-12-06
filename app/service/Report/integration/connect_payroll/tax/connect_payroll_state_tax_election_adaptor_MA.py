from .connect_payroll_state_tax_election_adaptor_base import ConnectPayrollStateTaxElectionAdaptorBase


class ConnectPayrollStateTaxElectionAdaptorMA(ConnectPayrollStateTaxElectionAdaptorBase):

    def __init__(self, state, state_tax_election):
        super(ConnectPayrollStateTaxElectionAdaptorMA, self).__init__(state, state_tax_election)
        self.election_data = state_tax_election

    def get_filing_status(self):
        if (self.election_data.head_of_household):
            return 'H'
        elif (self.election_data.spouse_exemption):
            return 'M'
        else:
            return 'S'

    def get_total_exemptions(self):
        return self.election_data.total_exemption

    def get_additional_exemptions(self):
        return None

    def get_additional_amount_code(self):
        return 'A'

    def get_additional_amount(self):
        return self.election_data.additional_witholding
