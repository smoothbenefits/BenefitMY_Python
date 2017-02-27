from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives

from .event_handler_base import EventHandlerBase
from ..events.environment_test_event import EnvironmentTestEvent


class EnvironmentTestEventHandler(EventHandlerBase):
    def __init__(self):
        super(EnvironmentTestEventHandler, self).__init__(EnvironmentTestEvent)
    
    def handle(self, event_message):
        print 'Start handling message ...'
        print event_message
        subject = "Test Event Handler"
        text_content = "Test Content"
        from_email = settings.SUPPORT_EMAIL_ADDRESS
        to_emails = ['jeff.zhang.82@gmail.com']
        msg = EmailMultiAlternatives(subject, text_content, from_email, to_emails)
        msg.send()
