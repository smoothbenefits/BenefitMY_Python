class EmployeeStateTaxInfo(object):

    def __init__(self, employee_state_tax_election_models):
        self._state_elections = {}

        for state_election_model in employee_state_tax_election_models:
            self._state_elections[state_election_model.state] = state_election_model.tax_election_data

    def get_election_data_for_state(self, state):
        if (state not in self._state_elections):
            return None
        return self._state_elections[state]

    def get_all_state_elections(self):
        return self._state_elections
