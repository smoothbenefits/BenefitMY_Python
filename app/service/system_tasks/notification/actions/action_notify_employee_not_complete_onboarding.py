from django.conf import settings
from django.contrib.auth import get_user_model
from app.models.company import Company
from app.service.hash_key_service import HashKeyService
from app.service.send_email_service import SendEmailService
from ...action_base import ActionBase

User = get_user_model()


class ActionNotifyEmployeeNotCompleteOnboarding(ActionBase):
    def __init__(self):
        super(ActionNotifyEmployeeNotCompleteOnboarding, self).__init__()

    def execute(self, action_data):
        if (not action_data
            or not 'company_user_id_list' in action_data):
            raise ValueError("action_data must contains valid 'company_user_id_list'!")

        send_email_service = SendEmailService()

        subject = '[Action Required] Onboarding not Completed'
        html_template_path = 'email/system_notifications/employee_not_complete_onboarding.html'
        txt_template_path = 'email/system_notifications/employee_not_complete_onboarding.txt'

        for company_id in action_data['company_user_id_list']:

            self.log.debug("Company {0}".format(company_id))
            user_id_list = action_data['company_user_id_list'][company_id]

            for user_id in user_id_list:

                self.log.debug("User {0}".format(user_id))
                context_data = { 'company': Company.objects.get(pk=company_id) }

                # build the list of target emails
                email = send_email_service.get_email_address_by_user(user_id)
                emails = [email]

                # build the template context data
                context_data = {'context_data':context_data, 'site_url':self._get_site_URL(user_id)}

                send_email_service.send_support_email(
                    emails, subject, context_data, html_template_path, txt_template_path)

                self.log.info("Action {0} ran to completion for user {1}".format(
                    self.__class__.__name__,
                    user_id))

        self.log.info("Action {0} ran to completion.".format(self.__class__.__name__))


    def _get_site_URL(self, user_id):
        user = User.objects.get(pk=user_id)
        if user.check_password(settings.DEFAULT_USER_PW):
            hash_key_service = HashKeyService()
            return "%semployee/signup/%s" % (settings.SITE_URL, hash_key_service.encode_key(user_id))
        return settings.SITE_URL
