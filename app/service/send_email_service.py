from datetime import datetime
from StringIO import StringIO
from django.contrib.auth import get_user_model
from django import template
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import get_template
from django.contrib.auth import get_user_model

from app.models.person import (Person, SELF)
from app.models.company_user import CompanyUser, USER_TYPE_ADMIN, USER_TYPE_BROKER
from app.service.Report.company_employee_benefit_pdf_report_service import \
    CompanyEmployeeBenefitPdfReportService

from app.models.system.email_block_list import (
    EmailBlockList,
    EMAIL_BLOCK_FEATURE_WORKTIMESHEETNOTIFICATION
)

User = get_user_model()


class SendEmailService(object):

    def send_support_email(
        self,
        to_emails,
        subject,
        email_template_context_data,
        html_template_path,
        text_template_path,
        attachment_name=None,
        attachment=None,
        attachment_mime_type=None,
        include_bm_support_email_address=True
    ):
        # Prepare and send the email with both HTML and plain text contents
        
        # Indicate, in the subject line, that the email is from non-production 
        # environment and hence is for testing only.
        if not settings.IS_PRODUCTION_ENVIRONMENT:
            subject = '[For Test]' + subject
        from_email = settings.SUPPORT_EMAIL_ADDRESS
        context = template.Context(email_template_context_data)
        html_template = get_template(html_template_path)
        html_content = html_template.render(context)
        text_template = get_template(text_template_path)
        text_content = text_template.render(context)

        # make sure to send our support email address a copy
        if (include_bm_support_email_address):
            to_emails.append(settings.SUPPORT_EMAIL_ADDRESS)

        msg = EmailMultiAlternatives(subject, text_content, from_email, to_emails)
        msg.attach_alternative(html_content, 'text/html')

        if (attachment_name is not None and attachment is not None and attachment_mime_type is not None):
            msg.attach(attachment_name, attachment, attachment_mime_type)

        msg.send()

    def get_employer_emails_by_company(self, company_id):
        return self._get_emails_by_company_user_type(company_id, USER_TYPE_ADMIN)

    def get_broker_emails_by_company(self, company_id):
        return self._get_emails_by_company_user_type(company_id, USER_TYPE_BROKER)

    def _get_emails_by_company_user_type(self, company_id, user_type):
        emails = []

        comp_users = CompanyUser.objects.filter(
            company=company_id,
            company_user_type=user_type)
        for comp_user in comp_users:
            email = self.get_email_address_by_user(comp_user.user_id)
            emails.append(email)

        return emails

    ''' Get the email address to use for the given user
    '''
    def get_email_address_by_user(self, user_id):
        user = User.objects.get(pk=user_id)
        email = user.email
        person = Person.objects.filter(user=user_id, relationship='self')
        if (len(person) > 0 and person[0].email):
            email = person[0].email
        return email

    ''' Get a basic version of email context data that contain
        some commonly used information such as site URL
    '''
    def _get_base_email_context_data(self):
        return {
            'site_url':settings.SITE_URL
        }

    def send_employee_benefit_group_update_notification_email(self, user, company, original_group, updated_group):

        group_member_change_info = {
            'user': user,
            'company': company,
            'original_company_group': original_group,
            'updated_company_group': updated_group
        }

        subject = 'Employee Benefit Group Change Notification'
        html_template_path = 'email/employee_benefit_group_change_notification.html'
        txt_template_path = 'email/employee_benefit_group_change_notification.txt'

        # build the list of target emails
        to_emails = self.get_broker_emails_by_company(group_member_change_info['company'].id)

        # get person data from user
        group_member_change_info['person'] = group_member_change_info['user'].family.filter(relationship=SELF).first()
        if (not group_member_change_info['person']):
            # Use the user information if the account does not have person profile
            # setup
            group_member_change_info['person'] = group_member_change_info['user']

        # build the template context data
        context_data = self._get_base_email_context_data()
        context_data['group_member_change_info'] = group_member_change_info

        # get PDF
        pdf_service = CompanyEmployeeBenefitPdfReportService()
        pdf_buffer = StringIO()
        pdf_service.get_employee_report(
            group_member_change_info['user'].id,
            group_member_change_info['company'].id,
            pdf_buffer)
        pdf = pdf_buffer.getvalue()
        pdf_buffer.close()

        self.send_support_email(
            to_emails, subject, context_data, html_template_path, txt_template_path,
            attachment_name='employee_details.pdf', attachment=pdf, attachment_mime_type='application/pdf')

        return

    def is_email_feature_blocked_for_user(self, user_id, email_feature):
        result = EmailBlockList.objects.filter(user=user_id, email_block_feature=email_feature)
        return result.count() > 0

    def get_all_users_blocked_for_email_feature(self, email_feature):
        return EmailBlockList.objects.filter(email_block_feature=email_feature).values_list('user', flat=True).distinct()
