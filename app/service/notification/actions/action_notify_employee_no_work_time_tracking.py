from django.conf import settings
from django.contrib.auth import get_user_model
from app.models.company import Company
from action_notify_employee_base import ActionNotifyEmployeeBase
from app.dtos.notification.email_data import EmailData

User = get_user_model()

class ActionNotifyEmployeeNoWorkTimeTracking(ActionNotifyEmployeeBase):

    def __init__(self):
        super(ActionNotifyEmployeeNoWorkTimeTracking, self).__init__()

    def _get_email_data(self, company_id, user_id):
        subject = '[Action Required] Missing Work Timesheet'
        html_template_path = 'email/system_notifications/employee_no_work_time_tracking.html'
        txt_template_path = 'email/system_notifications/employee_no_work_time_tracking.txt'

        context_data = { 'company': Company.objects.get(pk=company_id) }
        context_data = {'context_data':context_data, 'site_url':self._get_site_URL(user_id)}

        return EmailData(subject, html_template_path, txt_template_path, context_data)
