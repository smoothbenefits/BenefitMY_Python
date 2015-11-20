class TriggerBase(object):
    def __init__(self):
        self._actions = []

    def append_action(self, action):
        self._actions.append(action)

    def examine_and_execute_actions(self):
        condition_met = self._examine_condition()
        if (condition_met):
            for action in self._actions:
                action.execute(self._get_action_data())

    def _examine_condition(self):
        raise NotImplementedError

    def _get_action_data(self):
        return {}
