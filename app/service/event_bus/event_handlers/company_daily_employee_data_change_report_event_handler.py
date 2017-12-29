from datetime import datetime, timedelta
from django.conf import settings

from app.models.company import Company
from app.dtos.notification.email_data import EmailData

from .event_handler_base import EventHandlerBase
from ..events.company_daily_employee_data_change_report_event import CompanyDailyEmployeeDataChangeReportEvent
from app.service.send_email_service import SendEmailService
from app.service.data_modification_service import DataModificationService


class CompanyDailyEmployeeDataChangeReportEventHandler(EventHandlerBase):

    def __init__(self):
        super(CompanyDailyEmployeeDataChangeReportEventHandler, self).__init__(CompanyDailyEmployeeDataChangeReportEvent)
        self._send_email_service = SendEmailService()
        self._data_modification_service = DataModificationService()
    
    def _internal_handle(self, event):
        if (not event.company_id):
            raise ValueError('The event is expected to provide company_id, which is missing!')

        emails = self._send_email_service.get_employer_emails_by_company(event.company_id)

        # Get employee data modification summery records
        mod_summaries = self._data_modification_service.employee_modifications_summary(event.company_id, 24 * 60)
        if (len(mod_summaries) <= 0):
            # No modifications detected. Do not send anything
            return

        email_data = self._get_email_data(event.company_id, mod_summaries)

        self._send_email_service.send_support_email(
            emails, email_data.subject, email_data.context_data,
            email_data.html_template_path, email_data.txt_template_path
        )

    def _get_email_data(self, company_id, data_modification_summaries):
        # Get display date
        date_text = self._get_display_date()

        # Now prepare the email content data
        subject = '[System Notification - {0}] Employee Data Change Notification'.format(date_text)

        html_template_path = 'email/user_data_change_notification.html'
        txt_template_path = 'email/user_data_change_notification.txt'

        company_users_collection = [{ 
            'company': Company.objects.get(pk=company_id),
            'mod_summary_list': data_modification_summaries,
        }]

        context_data = { 
            'date': date_text
        }
        context_data = {
            'context_data':context_data,
            'company_users_collection':company_users_collection,
            'site_url':settings.SITE_URL
        }

        return EmailData(subject, html_template_path, txt_template_path, context_data, False)    

    def _get_display_date(self):
        now = datetime.now()
        date = now - timedelta(hours=12)
        return date.strftime('%m/%d/%Y')
