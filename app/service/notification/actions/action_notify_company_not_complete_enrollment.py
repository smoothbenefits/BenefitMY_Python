from django.conf import settings
from django.contrib.auth import get_user_model
from app.service.send_email_service import SendEmailService
from app.models.company import Company
from app.models.person import (Person, SELF)
from action_base import ActionBase

User = get_user_model()


class ActionNotifyCompanyNotCompleteEnrollment(ActionBase):
    def execute(self, action_data):
        if (not action_data
            or not 'company_user_id_list' in action_data):
            raise ValueError("action_data must contains valid 'company_user_id_list'!")

        send_email_service = SendEmailService()

        subject = 'Notification: Employee Enrollments not Completed'
        html_template_path = 'email/system_notifications/company_not_complete_enrollment.html'
        txt_template_path = 'email/system_notifications/company_not_complete_enrollment.txt'

        for company_id in action_data['company_user_id_list']:
            user_id_list = action_data['company_user_id_list'][company_id]

            context_data = {
                'company': Company.objects.get(pk=company_id),
                'users': self._get_user_view_model_list(user_id_list)
            }

            # build the list of target emails
            emails = send_email_service.get_employer_emails_by_company(company_id)

            # build the template context data
            context_data = {'context_data':context_data, 'site_url':settings.SITE_URL}

            send_email_service.send_support_email(
                emails, subject, context_data, html_template_path, txt_template_path)

    def _get_user_view_model_list(self, user_id_list):
        model_list = []
        for user_id in user_id_list:
            user = User.objects.get(pk=user_id)
            person = None
            persons = Person.objects.filter(user=user.id, relationship=SELF)
            if (len(persons) > 0):
                person = persons[0]
            if (person):
                model_list.append(
                    {
                        'first_name': person.first_name,
                        'last_name': person.last_name,
                        'birth_date': person.birth_date
                    })
            else:
                model_list.append(
                    {
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'birth_date': ''
                    })

        return model_list
