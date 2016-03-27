from app.service.monitoring.logging_service import LoggingService


class ActionBase(object):

    def __init__(self):
        self.log = LoggingService()

    def execute(self, action_data):
        raise NotImplementedError
