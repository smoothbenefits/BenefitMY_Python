import datetime;

from django import template
from django.core.mail import send_mail

from app.models.company import Company
from app.models.company_user import CompanyUser
from app.models.person import Person
from app.models.phone import Phone
from app.models.address import Address
from app.models.user import User

from reversion.models import Revision

HTML_CONTENT = """

    <html>
        <head>
        </head>
        <body>
            <h3>Company: {{company.name}}</h3>
            <ul>
            {% for person in person_list %}
                <li>{{ person.first_name }}</li>
            {% endfor %}
            </ul>
        </body>
    </html>

"""

TEXT_CONTENT = """

Company: {{company.name}}

Users:
    {% for person in person_list %}
    - {{ person.first_name }}
    {% endfor %}

"""

''' Provides services to detect/collect modification to the
    data store, and provide surrounding services for this 
    info. 
'''
class DataModificationService(object):

    def employee_modifications_notify_employer_for_all_companies(self, in_last_num_minutes):
        company_list = self._get_all_companies()

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
                user = User.objects.get(pk=c_user.user_id)
                email = user.email
                person = Person.objects.filter(user=c_user, relationship='self')
                if (len(person) > 0 and person[0].email):
                    email = person[0].email
                self._send_notification_email(email, company_model, persons)

    def _send_notification_email(self, to_email, company_model, person_models):
        context = template.Context({'person_list': person_models, 'company': company_model})
        html_template = template.Template(HTML_CONTENT)
        html_content = html_template.render(context)
        text_template = template.Template(TEXT_CONTENT)
        text_content = text_template.render(context)
        send_mail('Users Data Change Notification', text_content, 'Support@benefitmy.com', [to_email], fail_silently=False, html_message=html_content)

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

    def _get_all_companies(self):
        return Company.objects.all()
