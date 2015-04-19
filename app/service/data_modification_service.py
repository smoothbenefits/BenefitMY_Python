import datetime;

from django import template
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import get_template

from app.models.company import Company
from app.models.company_user import CompanyUser
from app.models.person import Person
from app.models.phone import Phone
from app.models.address import Address
from app.models.user import User

from reversion.models import Revision

''' Provides services to detect/collect modification to the
    data store, and provide surrounding services for this 
    info. 
'''
class DataModificationService(object):

    ''' Send notification emails to all companies' employer users
    '''
    def employee_modifications_notify_employer_for_all_companies(self, in_last_num_minutes):
        company_list = Company.objects.all()

        for company in company_list:
            self._employee_mod_notify_employer_by_company(company, in_last_num_minutes)

    def _employee_mod_notify_employer_by_company(self, company_model, in_last_num_minutes):

        # Get the list of employee users made modifications in the search range 
        persons = self.employee_modifications_summary_person_info_only(company_model.id, in_last_num_minutes)
        
        if (len(persons) > 0):
            # Get the list of users (employers) to notify
            c_users = CompanyUser.objects.filter(company=company_model.id,
                                           company_user_type='admin')
            for c_user in c_users:
                email = self._get_email_address_by_user(c_user.user_id)
                self._send_notification_email(email, [{ 'company':company_model, 'persons':persons }])


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
            persons = self.employee_modifications_summary_person_info_only(company_id, in_last_num_minutes)
            if (len(persons) > 0):
                companies = Company.objects.filter(pk=company_id)
                if (len(companies) > 0):
                    company = companies[0]
                    company_users_collection.append({ 'company':company, 'persons':persons })

        # If there is something needs to be notified about, send the email
        if (len(company_users_collection) > 0):
            email = self._get_email_address_by_user(broker_user_id)
            self._send_notification_email(email, company_users_collection)

    ''' Actually send the email
    '''
    def _send_notification_email(self, to_email, company_users_collection):
        # Prepare and send the email with both HTML and plain text contents
        subject = 'Users Data Change Notification'
        from_email = 'Support@benefitmy.com'
        context = template.Context({'company_users_collection':company_users_collection, 'site_url':settings.SITE_URL})
        html_template = get_template('email/user_data_change_notification.html')
        html_content = html_template.render(context)
        text_template = get_template('email/user_data_change_notification.txt')
        text_content = text_template.render(context)
        send_mail(subject, text_content, from_email, [to_email], fail_silently=False, html_message=html_content)

    ''' Provide summerization of employee-made modifications
        For now, this produces a list of person information about employee users that
        made data modifications in the last X minutes specified by 'in_last_num_minutes'
    '''
    def employee_modifications_summary_person_info_only(self, company_id, in_last_num_minutes):
        employee_user_ids = []
        company_list = Company.objects.filter(pk=company_id)

        if (len(company_list) > 0):
            company = company_list[0]
            employee_user_ids = self._get_all_user_ids_made_modifications_for_company(company, in_last_num_minutes)

        persons = Person.objects.filter(user__in=employee_user_ids, relationship='self')

        return persons 

    def _get_all_user_ids_made_modifications_for_company(self, company, in_last_num_minutes):
        users = CompanyUser.objects.filter(company=company.id,
                                           company_user_type='employee').values('user')

        user_ids = Revision.objects.filter(user__in=users, date_created__gte=datetime.datetime.utcnow()-datetime.timedelta(minutes=in_last_num_minutes)).values('user')

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
