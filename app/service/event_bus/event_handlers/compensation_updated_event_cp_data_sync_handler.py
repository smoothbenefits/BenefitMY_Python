from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives

from .event_handler_base import EventHandlerBase
from ..events.compensation_updated_event import CompensationUpdatedEvent


class CompensationUpdatedEventCpDataSyncHandler(EventHandlerBase):
    def __init__(self):
        super(CompensationUpdatedEventCpDataSyncHandler, self).__init__(CompensationUpdatedEvent)
    
    def _internal_handle(self, event):
        subject = "Test CompensationUpdatedEvent Handler"
        text_content = 'user_id : {0}'.format(event.user_id)
        from_email = settings.SUPPORT_EMAIL_ADDRESS
        to_emails = ['jeff.zhang.82@gmail.com']
        msg = EmailMultiAlternatives(subject, text_content, from_email, to_emails)
        msg.send()
