from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives

from .event_handler_base import EventHandlerBase
from ..events.compensation_updated_event import CompensationUpdatedEvent


class CompensationUpdatedEventCpDataSyncHandler(EventHandlerBase):
    def __init__(self):
        super(CompensationUpdatedEventCpDataSyncHandler, self).__init__(CompensationUpdatedEvent)
    
    def _internal_handle(self, event):
        # TODO: 
        # Once we know how to sync compensation data to CP, we would then
        # implement logic here
        pass
