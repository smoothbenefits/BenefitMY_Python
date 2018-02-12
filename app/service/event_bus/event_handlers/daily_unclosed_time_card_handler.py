from django.conf import settings

from .event_handler_base import EventHandlerBase
from ..events.time_7am_utc_event import Time7AMUTCEvent
from app.service.time_punch_card_service import TimePunchCardService


class DailyUnclosedTimeCardHandler(EventHandlerBase):
    _time_punch_card_service = TimePunchCardService()

    def __init__(self):
        super(DailyUnclosedTimeCardHandler, self).__init__(Time7AMUTCEvent)
    
    def _internal_handle(self, event):
        # Connect with TimeCard service synchronously
        handled = self._time_punch_card_service.handle_unclosed_time_cards()
        if handled:
            self._logger.info('System closed {} unclosed time cards'.format(handled.get('handled_count', '-1')))
        else:
            self._logger.error('System encountered error when trying to handle unclosed time cards!')
