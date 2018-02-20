import datetime;

from django import template
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import get_template
from django.contrib.auth import get_user_model

from app.models.company import Company
from app.models.company_user import CompanyUser
from app.models.person import Person
from app.models.phone import Phone
from app.models.address import Address
from app.service.send_email_service import SendEmailService
from app.service.user_enrollment_summary_service import (
    UserEnrollmentSummaryService,
    NO_BENEFITS
)
from app.service.user_onboarding_state_service import UserOnboardingStateService
from reversion.models import Revision

User = get_user_model()

''' Provides services to detect/collect modification to the
    data store, and provide surrounding services for this
    info.
'''
class DataModificationService(object):

    ''' Send notification emails for employee modifications to specific email addresses
    '''
    def employee_modifications_notify_specific_target(self, in_last_num_minutes, target_emails):
        company_list = Company.objects.all()
        for company in company_list:
            self._employee_mod_notify_target_by_company(company, in_last_num_minutes, target_emails)

    ''' Send notification emails to all companies' employer users
    '''
    def employee_modifications_notify_employer_for_all_companies(self, in_last_num_minutes):
        email_service = SendEmailService()
        company_list = Company.objects.all()
        for company in company_list:
            emails = email_service.get_employer_emails_by_company(company.id)
            self._employee_mod_notify_target_by_company(company, in_last_num_minutes, emails)

    def _employee_mod_notify_target_by_company(self, company_model, in_last_num_minutes, target_emails):

        # Get the list of employee users made modifications in the search range
        mod_summaries = self.employee_modifications_summary(company_model.id, in_last_num_minutes)
        if (len(mod_summaries) > 0):
            self._send_notification_email(target_emails, [{ 'company':company_model, 'mod_summary_list':mod_summaries }])

    ''' Send email notification to all brokers.
        All clients of each broker would have the relevant notification data
        aggregated into 1 email
    '''
    def employee_modifications_notify_all_brokers(self, in_last_num_minutes):
        broker_user_ids = CompanyUser.objects.filter(company_user_type='broker').values_list('user', flat=True).distinct()

        for broker_user_id in broker_user_ids:
            self._employee_mod_notify_broker(broker_user_id, in_last_num_minutes)

    def _employee_mod_notify_broker(self, broker_user_id, in_last_num_minutes):
        company_ids = CompanyUser.objects.filter(company_user_type='broker', user=broker_user_id).values_list('company', flat=True).distinct()

        # The result collection of data to bind to the email content
        # Each entry will be for 1 client company
        company_users_collection = []
        for company_id in company_ids:
            # Get the list of employee users made modifications in the search range
            mod_summaries = self.employee_modifications_summary(company_id, in_last_num_minutes)
            if (len(mod_summaries) > 0):
                companies = Company.objects.filter(pk=company_id)
                if (len(companies) > 0):
                    company = companies[0]
                    company_users_collection.append({ 'company':company, 'mod_summary_list':mod_summaries })

        # If there is something needs to be notified about, send the email
        if (len(company_users_collection) > 0):
            email_service = SendEmailService()
            emails = [email_service.get_email_address_by_user(broker_user_id)]
            self._send_notification_email(emails, company_users_collection)

    ''' Actually send the email
    '''
    def _send_notification_email(self, to_email_list, company_users_collection):
        email_service = SendEmailService()

        # Prepare and send the email with both HTML and plain text contents
        subject = 'Users Data Change Notification'
        from_email = 'Support@benefitmy.com'
        context_data = {'company_users_collection':company_users_collection, 'site_url':settings.SITE_URL}
        html_template_path = 'email/user_data_change_notification.html'
        text_template_path = 'email/user_data_change_notification.txt'

        email_service.send_support_email(
            to_email_list,
            subject,
            context_data,
            html_template_path,
            text_template_path
        )

    ''' Provide summerization of employee-made modifications
        For now, this produces a list of person information about employee users that
        made data modifications in the last X minutes specified by 'in_last_num_minutes'
    '''
    def employee_modifications_summary(self, company_id, in_last_num_minutes):
        employee_user_ids = []
        company_list = Company.objects.filter(pk=company_id)

        if (len(company_list) > 0):
            company = company_list[0]
            employee_user_ids = self._get_all_user_ids_made_modifications_for_company(company, in_last_num_minutes)
        mod_summary_list = []
        for user_item in employee_user_ids:
            user_id = user_item['user']
            mod_summary={}
            persons = Person.objects.filter(user=user_id, relationship='self')
            if persons:
                mod_summary['person'] = persons[0]
                enrollment_status = self._get_enrollment_status(user_id, persons[0], company_id)
                mod_summary['enrollmentStatus'] = enrollment_status
                mod_summary['hasBenefits'] = (not enrollment_status == NO_BENEFITS) 
                mod_summary['onboardingStatus'] = 'NOT_COMPLETE'
                if self._has_user_completed_onboarding(user_id):
                    mod_summary['onboardingStatus'] = 'COMPLETE'
                mod_summary_list.append(mod_summary)
        return mod_summary_list

    def _get_all_user_ids_made_modifications_for_company(self, company, in_last_num_minutes):
        users = CompanyUser.objects.filter(company=company.id,
                                           company_user_type='employee').values('user')

        user_ids = Revision.objects.filter(user__in=users, date_created__gte=datetime.datetime.utcnow()-datetime.timedelta(minutes=in_last_num_minutes)).distinct().values('user')

        return user_ids

    ''' Get the email address to use for the given user
    '''
    def _get_email_address_by_user(self, user_id):
        user = User.objects.get(pk=user_id)
        email = user.email
        person = Person.objects.filter(user=user_id, relationship='self')
        if (len(person) > 0 and person[0].email):
            email = person[0].email
        return email

    def _get_enrollment_status(self, user_id, person, company_id):
        enrollment_status_service = UserEnrollmentSummaryService(company_id, user_id, person.id)
        return enrollment_status_service.get_enrollment_status()

    def _has_user_completed_onboarding(self, user_id):
        onboarding_state_service = UserOnboardingStateService()
        return onboarding_state_service.has_onboarding_process_completed_by_user(user_id)
