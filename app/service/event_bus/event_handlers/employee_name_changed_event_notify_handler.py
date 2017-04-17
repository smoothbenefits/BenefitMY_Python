from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives

from .event_handler_base import EventHandlerBase
from ..events.employee_name_changed_event import EmployeeNameChangedEvent

class EmployeeNameChangedEventNotifyHandler(EventHandlerBase):
    def __init__(self):
        super(EmployeeNameChangedEventNotifyHandler, self).__init__(EmployeeNameChangedEvent)
    
    def handle(self, event):
        subject = "Employee Name Changed!"
        text_content = 'Original Name: {0}; New Name: {1}'.format(event.original_value, event.updated_value)
        from_email = settings.SUPPORT_EMAIL_ADDRESS
        to_emails = ['jeff.zhang.82@gmail.com']
        msg = EmailMultiAlternatives(subject, text_content, from_email, to_emails)
        msg.send()
