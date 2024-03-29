from django.conf import settings
from django.contrib.auth import get_user_model
from app.service.send_email_service import SendEmailService
from app.models.company import Company
from app.models.person import (Person, SELF)
from ...action_base import ActionBase

User = get_user_model()


class ActionNotifyCompanyBase(ActionBase):
    def __init__(self):
        super(ActionNotifyCompanyBase, self).__init__()

    def execute(self, action_data):
        if (not action_data
            or not 'company_user_id_list' in action_data):
            raise ValueError("action_data must contains valid 'company_user_id_list'!")

        send_email_service = SendEmailService()

        for company_id in action_data['company_user_id_list']:
            user_id_list = action_data['company_user_id_list'][company_id]

            email_data = self._get_email_data(company_id, user_id_list)

            # build the list of target emails
            emails = send_email_service.get_employer_emails_by_company(company_id)
            if email_data.include_broker:
                broker_emails = send_email_service.get_broker_emails_by_company(company_id)
                emails.extend(broker_emails)

            send_email_service.send_support_email(
                emails, email_data.subject, email_data.context_data,
                email_data.html_template_path, email_data.txt_template_path)

            self.log.info("Action {} ran to completion for company {}".format(
                self.__class__.__name__, company_id
            ))

        self.log.info("Action {} ran to completion".format(self.__class__.__name__))

    def _get_email_data(self, company_id, user_id_list):
        raise NotImplementedError()

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
