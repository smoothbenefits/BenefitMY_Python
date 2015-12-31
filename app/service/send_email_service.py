from datetime import datetime
from django.contrib.auth import get_user_model
from django import template
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import get_template
from django.contrib.auth import get_user_model

from app.models.person import Person
from app.models.company_user import CompanyUser, USER_TYPE_ADMIN, USER_TYPE_BROKER

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
