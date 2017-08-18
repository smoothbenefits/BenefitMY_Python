from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives

from .event_handler_base import EventHandlerBase
from ..events.employee_profile_updated_event import EmployeeProfileUpdatedEvent


class EmployeeProfileUpdatedEventCpDataSyncHandler(EventHandlerBase):
    def __init__(self):
        super(EmployeeProfileUpdatedEventCpDataSyncHandler, self).__init__(EmployeeProfileUpdatedEvent)
    
    def _internal_handle(self, event):
        subject = "Test EmployeeProfileUpdatedEvent Handler"
        text_content = '{0} : {1}'.format(event.user_id, event.company_id)
        from_email = settings.SUPPORT_EMAIL_ADDRESS
        to_emails = ['jeff.zhang.82@gmail.com']
        msg = EmailMultiAlternatives(subject, text_content, from_email, to_emails)
        msg.send()
