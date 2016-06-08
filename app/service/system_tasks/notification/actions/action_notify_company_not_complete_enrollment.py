from django.conf import settings
from app.models.company import Company
from action_notify_company_base import ActionNotifyCompanyBase
from app.dtos.notification.email_data import EmailData


class ActionNotifyCompanyNotCompleteEnrollment(ActionNotifyCompanyBase):
    
    def __init__(self):
        super(ActionNotifyCompanyNotCompleteEnrollment, self).__init__()

    def _get_email_data(self, company_id, user_id_list):
        subject = '[Action Required] Employee Enrollments not Completed'
        html_template_path = 'email/system_notifications/company_not_complete_enrollment.html'
        txt_template_path = 'email/system_notifications/company_not_complete_enrollment.txt'

        context_data = {
            'company': Company.objects.get(pk=company_id),
            'users': self._get_user_view_model_list(user_id_list)
        }

        # build the template context data
        context_data = {'context_data':context_data, 'site_url':settings.SITE_URL}

        email_data = EmailData(subject, html_template_path, txt_template_path, context_data, True)
        return email_data
