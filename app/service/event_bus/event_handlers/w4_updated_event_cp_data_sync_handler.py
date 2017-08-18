from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives

from .event_handler_base import EventHandlerBase
from ..events.w4_updated_event import W4UpdatedEvent


class W4UpdatedEventCpDataSyncHandler(EventHandlerBase):
    def __init__(self):
        super(W4UpdatedEventCpDataSyncHandler, self).__init__(W4UpdatedEvent)
    
    def _internal_handle(self, event):
        subject = "Test W4UpdatedEvent Handler"
        text_content = 'user_id : {0}'.format(event.user_id)
        from_email = settings.SUPPORT_EMAIL_ADDRESS
        to_emails = ['jeff.zhang.82@gmail.com']
        msg = EmailMultiAlternatives(subject, text_content, from_email, to_emails)
        msg.send()
