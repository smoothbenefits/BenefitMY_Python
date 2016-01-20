import logging
from logentries import LogentriesHandler
from django.conf import settings

class LoggingService(object):

    def __init__(self):
        self.log = logging.getLogger('LogEntriesLogger')
        self.log.setLevel(logging.INFO)
        logHandler = LogentriesHandler(settings.LOGENTRIES_TOKEN)
        self.log.addHandler(logHandler)

    def error(self, message):
        self.log.error(message)

    def warn(self, message):
        self.log.warn(message)

    def info(self, message):
        print self.log
        self.log.info(message)

    def debug(self, message):
        self.log.debug(message)
