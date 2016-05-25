from app.service.monitoring.logging_service import LoggingService


class TriggerBase(object):
    def __init__(self):
        self._actions = []
        self.log = LoggingService()

    def has_actions(self):
        return len(self._actions) > 0

    def append_action(self, action):
        self._actions.append(action)

    def examine_and_execute_actions(self):
        condition_met = self._examine_condition()

        self.log.info("Trigger {} met condition? {}".format(
            self.__class__.__name__, condition_met
        ))

        if (condition_met):
            for action in self._actions:
                self.log.debug("Action " + type(action).__name__)
                action.execute(self._get_action_data())

    def _examine_condition(self):
        raise NotImplementedError

    def _get_action_data(self):
        return {}
