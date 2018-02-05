from .connect_payroll_state_tax_election_adaptor_MA import ConnectPayrollStateTaxElectionAdaptorMA
from .connect_payroll_state_tax_election_adaptor_RI import ConnectPayrollStateTaxElectionAdaptorRI
from .connect_payroll_state_tax_election_adaptor_import import ConnectPayrollStateTaxElectionAdaptorImport


class ConnectPayrollStateTaxElectionAdaptorFactory(object):
    
    # This serves as the list of states that we currently support
    # state tax election export
    # [Remark]: As of Oct 2017, WBM only supports RI and MA state tax
    _state_adaptor_class_map = {
        'MA': ConnectPayrollStateTaxElectionAdaptorMA,
        'RI': ConnectPayrollStateTaxElectionAdaptorRI
    }

    def __init__(self):
        pass

    def get_adaptor(self, state, state_tax_election_data):
        if (state not in self._state_adaptor_class_map):
            return None

        adaptor = self._state_adaptor_class_map[state]
        if (state_tax_election_data.is_imported):
            adaptor = ConnectPayrollStateTaxElectionAdaptorImport
        return adaptor(state, state_tax_election_data)
