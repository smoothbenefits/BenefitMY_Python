from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives

from .event_handler_base import EventHandlerBase
from ..events.person_info_updated_event import PersonInfoUpdatedEvent


class PersonInfoUpdatedEventCpDataSyncHandler(EventHandlerBase):
    def __init__(self):
        super(PersonInfoUpdatedEventCpDataSyncHandler, self).__init__(PersonInfoUpdatedEvent)
    
    def _internal_handle(self, event):
        subject = "Test PersonInfoUpdatedEvent Handler"
        text_content = 'person_id : {0}'.format(event.person_id)
        from_email = settings.SUPPORT_EMAIL_ADDRESS
        to_emails = ['jeff.zhang.82@gmail.com']
        msg = EmailMultiAlternatives(subject, text_content, from_email, to_emails)
        msg.send()
