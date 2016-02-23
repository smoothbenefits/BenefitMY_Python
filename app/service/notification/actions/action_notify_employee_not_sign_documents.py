from django.conf import settings
from django.contrib.auth import get_user_model
from app.models.company import Company
from action_notify_employee_base import ActionNotifyEmployeeBase
from app.dtos.notifaction.email_data import EmailData

User = get_user_model()

class ActionNotifyEmployeeNotSignDocument(ActionNotifyEmployeeBase):

    def __init__(self):
        super(ActionNotifyEmployeeNotSignDocuments, self).__init__()

    def _get_email_data(self, company_id, user_id):
        subject = '[Action Required] Document not Signed'
        html_template_path = 'email/system_notifications/employee_not_sign_document.html'
        txt_template_path = 'email/system_notifications/employee_not_sign_document.txt'

        context_data = { 'company': Company.objects.get(pk=company_id) }
        context_data = {'context_data':context_data, 'site_url':self._get_site_URL(user_id)}

        return EmailData(subject, html_template_path, txt_template_path, context_data)

    def _get_site_URL(self, user_id):
        user = User.objects.get(pk=user_id)
        if user.check_password(settings.DEFAULT_USER_PW):
            hash_key_service = HashKeyService()
            return "%semployee/signup/%s" % (settings.SITE_URL, hash_key_service.encode_key(user_id))
        return settings.SITE_URL
