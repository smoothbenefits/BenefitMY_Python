import json
import traceback
from datetime import datetime
from app.service.monitoring.logging_service import LoggingService


class EventHandlerBase(object):
    _logger = LoggingService()

    def __init__(self, event_class):
        ''' Requires to register the target class of
            the event this is handling
        ''' 
        self.event_class = event_class

    ''' Handle the event.
        Note: the event here an instance of the event_class
              registered for this handler.
    ''' 
    def handle(self, event):
        self._logger.info('Begin handling event ...')
        self._logger.info(event)

        try:
            self._internal_handle(event)
            self._logger.info('Finished handling event')
        except Exception as e:
            self._logger.error(traceback.format_exc())
            raise

    def _internal_handle(self, event):
        raise NotImplementedError()
