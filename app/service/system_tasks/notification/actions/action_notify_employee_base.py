from django.conf import settings
from django.contrib.auth import get_user_model
from app.models.company import Company
from app.service.hash_key_service import HashKeyService
from app.service.send_email_service import SendEmailService
from ...action_base import ActionBase

User = get_user_model()


class ActionNotifyEmployeeBase(ActionBase):
    def __init__(self):
        super(ActionNotifyEmployeeBase, self).__init__()

    def execute(self, action_data):

        if (not action_data
            or not 'company_user_id_list' in action_data):
            raise ValueError("action_data must contains valid 'company_user_id_list'!")

        send_email_service = SendEmailService()

        for company_id in action_data['company_user_id_list']:
            user_id_list = action_data['company_user_id_list'][company_id]
            for user_id in user_id_list:
                # build the list of target emails
                email = send_email_service.get_email_address_by_user(user_id)
                emails = [email]
                # Get action dependent data for outbound emails
                email_data = self._get_email_data(company_id, user_id)
                send_email_service.send_support_email(
                    emails, email_data.subject, email_data.context_data,
                    email_data.html_template_path, email_data.txt_template_path
                )

                self.log.info("Action {} ran to completion for user {}".format(self.__class__.__name__, user_id))

        self.log.info("Action {} ran to completion.".format(self.__class__.__name__))

    def _get_site_URL(self, user_id):
        user = User.objects.get(pk=user_id)
        if user.check_password(settings.DEFAULT_USER_PW):
            hash_key_service = HashKeyService()
            return "%semployee/signup/%s" % (settings.SITE_URL, hash_key_service.encode_key(user_id))
        return settings.SITE_URL

    def _get_email_data(self, company_id, user_id):
        raise NotImplementedError()
