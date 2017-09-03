from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives

from .event_handler_base import EventHandlerBase
from ..events.environment_test_event import EnvironmentTestEvent


class EnvironmentTestEventHandler(EventHandlerBase):
    def __init__(self):
        super(EnvironmentTestEventHandler, self).__init__(EnvironmentTestEvent)
    
    def _internal_handle(self, event):
        # subject = "Test Event Handler"
        # text_content = event.host_url
        # from_email = settings.SUPPORT_EMAIL_ADDRESS
        # to_emails = []
        # msg = EmailMultiAlternatives(subject, text_content, from_email, to_emails)
        # msg.send()

        pass
