import logging

from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from django.contrib.auth import get_user_model


from .event_handler_base import EventHandlerBase
from ..events.punch_card_recognition_failed_event import PunchCardRecognitionFailedEvent
from ...send_email_service import SendEmailService
from ...hash_key_service import HashKeyService
from app.models.company_user import CompanyUser, USER_TYPE_ADMIN
from app.models.person import Person, SELF

User = get_user_model()

class PunchCardRecognitionFailedHandler(EventHandlerBase):
    def __init__(self):
        super(PunchCardRecognitionFailedHandler, self).__init__(PunchCardRecognitionFailedEvent)
        self.hash_key_service = HashKeyService()
        self.email_service = SendEmailService()

    def _get_admins_by_company(self, comp_id):
        comp_users = CompanyUser.objects.filter(company=comp_id, company_user_type=USER_TYPE_ADMIN)
        admins = []
        for comp_user in comp_users:
            admin_user = User.objects.get(pk=comp_user.user_id)
            admin_user_person = self._get_user_info_by_id(comp_user.user_id)
            if admin_user_person:
                admins.append(admin_user_person)
            else:
                admins.append(admin_user)
        return admins

    def _get_user_info_by_id(self, user_id):
        try:
            return Person.objects.get(user=user_id, relationship=SELF)
        except Person.DoesNotExist:
            return None

    def handle(self, event):
        if not event.company_id or not event.user_id:
            logging.warning(
                "Handling PunchCardRecognitionFailedEvent with no user_id nor company_id. Do nothing."
            )
            return

        logging.info(
            "Handling PunchCardRecognitionFailedEvent with company_id {}, user_id {}!".format(event.company_id, event.user_id)
        )
        subject = "Check in/out employee and photo mismatch"
        html_template = "email/punch_card_recognition_failed_notification.html"
        text_template = "email/punch_card_recognition_failed_notification.txt"
        admins = self._get_admins_by_company(self.hash_key_service.decode_key_with_environment(event.company_id))
        if len(admins) <= 0:
            logging.error(
                "PunchCardRecognitionFailedEvent failed. The company id {} passed in has no admin users".format(event.company_id)
            )
            return

        employee = self._get_user_info_by_id(self.hash_key_service.decode_key_with_environment(event.user_id))
        if not employee:
            logging.error(
                "PunchCardRecognitionFailedEvent failed. The employee of company {} cannot match passed in user_id {}".format(event.company_id, event.user_id)
            )
            return
        for admin in admins:
            context_data = {
                'admin': admin,
                'employee': employee,
                'card': {
                    'status': 'in' if event.in_progress else 'out',
                    'photo_url': event.photo_url
                }
            }
            
            to_emails = []
            to_emails.append(admin.email)
            self.email_service.send_support_email(
                to_emails,
                subject,
                context_data,
                html_template,
                text_template
            )
