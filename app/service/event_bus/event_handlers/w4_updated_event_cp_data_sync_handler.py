from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives

from .event_handler_base import EventHandlerBase
from ..events.w4_updated_event import W4UpdatedEvent


class W4UpdatedEventCpDataSyncHandler(EventHandlerBase):
    def __init__(self):
        super(W4UpdatedEventCpDataSyncHandler, self).__init__(W4UpdatedEvent)
    
    def _internal_handle(self, event):
        # TODO: 
        # Once we know how to sync W4 data to CP, we would then
        # implement logic here
        pass
