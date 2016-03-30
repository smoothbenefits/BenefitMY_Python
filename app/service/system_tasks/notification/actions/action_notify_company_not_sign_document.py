from django.conf import settings
from django.contrib.auth import get_user_model
from app.service.send_email_service import SendEmailService
from app.models.company import Company
from app.models.person import (Person, SELF)
from action_notify_company_base import ActionNotifyCompanyBase
from app.dtos.notification.email_data import EmailData

User = get_user_model()

class ActionNotifyCompanyNotSignDocument(ActionNotifyCompanyBase):

    def __init__(self):
        super(ActionNotifyCompanyNotSignDocument, self).__init__()

    def _get_email_data(self, company_id, user_id_list):

        subject = '[Action Required] Employee Document not Signed'
        html_template_path = 'email/system_notifications/company_not_sign_document.html'
        txt_template_path = 'email/system_notifications/company_not_sign_document.txt'

        context_data = {
            'company': Company.objects.get(pk=company_id),
            'users': self._get_user_view_model_list(user_id_list)
        }

        # build the template context data
        context_data = {'context_data':context_data, 'site_url':settings.SITE_URL}

        email_data = EmailData(subject, html_template_path, txt_template_path, context_data)
        return email_data

    def _get_user_view_model_list(self, user_id_list):
        send_email_service = SendEmailService()
        model_list = []
        for user_id in user_id_list:
            user = User.objects.get(pk=user_id)
            email = send_email_service.get_email_address_by_user(user_id)
            person = None
            persons = Person.objects.filter(user=user.id, relationship=SELF)
            if (len(persons) > 0):
                person = persons[0]
            if (person):
                model_list.append(
                    {
                        'first_name': person.first_name,
                        'last_name': person.last_name,
                        'email': email
                    })
            else:
                model_list.append(
                    {
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'email': email
                    })

        return model_list
