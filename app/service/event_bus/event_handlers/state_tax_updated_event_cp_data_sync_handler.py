from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives

from .event_handler_base import EventHandlerBase
from ..events.state_tax_updated_event import StateTaxUpdatedEvent


class StateTaxUpdatedEventCpDataSyncHandler(EventHandlerBase):
    def __init__(self):
        super(StateTaxUpdatedEventCpDataSyncHandler, self).__init__(StateTaxUpdatedEvent)
    
    def _internal_handle(self, event):
        # TODO: 
        # Once we know how to sync state tax data to CP, we would then
        # implement logic here
        pass
