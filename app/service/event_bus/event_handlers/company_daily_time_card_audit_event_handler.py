from datetime import datetime, timedelta
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives

from app.models.company import Company
from app.dtos.notification.email_data import EmailData
from app.view_models.time_tracking.time_card_validation_issue import TimeCardValidationIssue

from .event_handler_base import EventHandlerBase
from ..events.company_daily_time_card_audit_requested_event import CompanyDailyTimeCardAuditEvent
from app.service.time_punch_card_service import TimePunchCardService
from app.service.send_email_service import SendEmailService


class CompanyDailyTimeCardAuditEventHandler(EventHandlerBase):

    def __init__(self):
        super(CompanyDailyTimeCardAuditEventHandler, self).__init__(CompanyDailyTimeCardAuditEvent)
        self._time_punch_card_service = TimePunchCardService()
        self._send_email_service = SendEmailService()
    
    def _internal_handle(self, event):
        if (not event.company_id):
            raise ValueError('The event is expected to provide company_id, which is missing!')

        emails = self._send_email_service.get_employer_emails_by_company(event.company_id)
        email_data = self._get_email_data(event.company_id)

        self._send_email_service.send_support_email(
            emails, email_data.subject, email_data.context_data,
            email_data.html_template_path, email_data.txt_template_path
        )

    def _get_email_data(self, company_id):
        # Get cards with validation issues
        card_aggrgates_with_issues = self._get_time_cards_aggrgates_with_issues(company_id)

        # Get display date
        date_text = self._get_display_date()

        # Now prepare the email content data
        subject = '[System Notification - {0}] Time & Attendance Data Validation Result'.format(date_text)

        html_template_path = 'email/system_notifications/time_card_audit_notification.html'
        txt_template_path = 'email/system_notifications/time_card_audit_notification.txt'

        context_data = { 
            'company': Company.objects.get(pk=company_id),
            'card_aggrgates_with_issues': card_aggrgates_with_issues,
            'date': date_text
        }
        context_data = {'context_data':context_data, 'site_url':settings.SITE_URL}

        return EmailData(subject, html_template_path, txt_template_path, context_data, False)    

    def _get_time_cards_aggrgates_with_issues(self, company_id):
        # Get all cards for the company for the day just passed
        # The assumption is that this report would be run sometime near
        # the end of the day. Just to play safe that this is not ran just
        # a few minutes passed the calendar day mark, take a time 12 hours
        # earlier to ensure we are looking at the right date.
        now = datetime.now()
        card_date = now - timedelta(hours=12)

        card_aggregates = self._time_punch_card_service.get_company_users_daily_time_punch_cards_aggregates(
                company_id,
                card_date,
                include_unclosed_cards=True)

        card_aggregates_with_issues = [_TimeCardAggregateViewModel(card_aggregate) for card_aggregate in card_aggregates if len(card_aggregate.validation_issues) > 0]

        return card_aggregates_with_issues

    def _get_display_date(self):
        now = datetime.now()
        date = now - timedelta(hours=12)
        return date.strftime('%m/%d/%Y')


class _TimeCardAggregateViewModel(object):
    def __init__(self, time_punch_card_aggregate):
        self.employee_full_name = time_punch_card_aggregate.employee_full_name
        self.validation_issues = [_TimeCardValidationIssueViewModel(issue) for issue in time_punch_card_aggregate.validation_issues]


class _TimeCardValidationIssueViewModel(object):
    def __init__(self, validation_issue):
        self.notes = validation_issue.notes
        self.level = validation_issue.level
        self.visual_cue_css_class = 'circle_unknown'
        
        if (self.level == TimeCardValidationIssue.LEVEL_ERROR):
            self.visual_cue_css_class = 'circle_error'
        elif (self.level == TimeCardValidationIssue.LEVEL_WARNING):
            self.visual_cue_css_class = 'circle_warning'
