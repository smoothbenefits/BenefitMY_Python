from ..monitoring.logging_service import LoggingService

log = LoggingService()


''' Base implementation of facility to manage system tasks of
    different types
'''
class SystemTaskServiceBase(object):
    def __init__(self):
        # Initialize all the trigger to action links here
        # This can potentially be exposed to consumers of
        # the service, but don't see the need to delegate
        # this now.
        self._triggers = []

    def register_trigger(self, trigger):
        if (not trigger or not trigger.has_actions()):
            raise ValueError('The specified trigger is not valid!')

        self._triggers.append(trigger)

    def execute(self):
        for trigger in self._triggers:
            trigger.examine_and_execute_actions()
            log.info("Finished trigger {}".format(type(trigger).__name__))
