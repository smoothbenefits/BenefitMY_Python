from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives

from .event_handler_base import EventHandlerBase
from ..events.environment_test_event import EnvironmentTestEvent


class AnotherEnvironmentTestEventHandler(EventHandlerBase):
    def __init__(self):
        super(AnotherEnvironmentTestEventHandler, self).__init__(EnvironmentTestEvent)
    
    def handle(self, event):
        # subject = "Test Event Handler"
        # text_content = event.environment
        # from_email = settings.SUPPORT_EMAIL_ADDRESS
        # to_emails = []
        # msg = EmailMultiAlternatives(subject, text_content, from_email, to_emails)
        # msg.send()

        pass
