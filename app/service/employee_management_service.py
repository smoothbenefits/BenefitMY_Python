from datetime import datetime
from StringIO import StringIO
from django.contrib.auth import get_user_model
from django import template
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import get_template
from django.contrib.auth import get_user_model

from app.models.employee_profile import (
    EmployeeProfile,
    EMPLOYMENT_STATUS_TERMINATED)
from app.dtos.operation_result import OperationResult
from app.service.send_email_service import SendEmailService
from app.service.Report.company_employee_benefit_pdf_report_service import \
    CompanyEmployeeBenefitPdfReportService

User = get_user_model()


class EmployeeManagementService(object):
    def terminate_employee(self, termination_data):
        result = OperationResult(termination_data)
        employee_profiles = EmployeeProfile.objects.filter(
            person=termination_data.person_id,
            company=termination_data.company_id)

        if (len(employee_profiles) <= 0):
            raise Exception('Could not locate employee profile for person [%s]' % termination_data.person_id)

        employee_profile = employee_profiles[0]
        employee_profile.end_date = termination_data.end_date
        employee_profile.employment_status = EMPLOYMENT_STATUS_TERMINATED
        employee_profile.save()

        result.set_output_data(employee_profile)

        # Now send termination email
        self._send_termination_email(employee_profile)

        return result

    def _send_termination_email(self, employee_profile_model):
        send_email_service = SendEmailService()

        subject = 'Employment Termination Notification'
        html_template_path = 'email/employment_termination_notification.html'
        txt_template_path = 'email/employment_termination_notification.txt'

        # build the list of target emails
        to_emails = []
        employer_emails = send_email_service.get_employer_emails_by_company(employee_profile_model.company.id)
        to_emails.extend(employer_emails)
        broker_emails = send_email_service.get_broker_emails_by_company(employee_profile_model.company.id)
        to_emails.extend(broker_emails)

        # build the template context data
        context_data = {'employee_profile':employee_profile_model, 'site_url':settings.SITE_URL}

        # get PDF
        pdf_service = CompanyEmployeeBenefitPdfReportService()
        pdf_buffer = StringIO()
        pdf_service.get_employee_report(
            employee_profile_model.person.user.id,
            employee_profile_model.company.id,
            pdf_buffer)
        pdf = pdf_buffer.getvalue()
        pdf_buffer.close()

        send_email_service.send_support_email(
            to_emails, subject, context_data, html_template_path, txt_template_path,
            attachment_name='employee_details.pdf', attachment=pdf, attachment_mime_type='application/pdf')

        return
