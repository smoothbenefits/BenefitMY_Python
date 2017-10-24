from .connect_payroll_state_tax_election_adaptor_base import ConnectPayrollStateTaxElectionAdaptorBase


class ConnectPayrollStateTaxElectionAdaptorRI(ConnectPayrollStateTaxElectionAdaptorBase):

    def __init__(self, state, state_tax_election):
        super(ConnectPayrollStateTaxElectionAdaptorRI, self).__init__(state, state_tax_election)

    def get_filing_status(self):
        return 'RI'

    def get_total_exemptions(self):
        return '5'

    def get_additional_exemptions(self):
        return '1'

    def get_additional_amount_code(self):
        return 'F'

    def get_additional_amount(self):
        return 3

