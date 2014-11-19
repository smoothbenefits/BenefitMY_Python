from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns


from app.views.person_view import PersonView
from app.views.user_view import (
    UserView,
    UsersView,
    UserFamilyView,
    CurrentUserView)
from app.views.company_user_view import (
    CompanyUserView,
    CompanyEmployeeCountView,
    BrokerCompanyCountView,
    CompanyBrokerCountView)
from app.views.benefit_type_view import BenefitTypeView
from app.views.document_type_view import DocumentTypeView
from app.views.company_view import (
    CompanyView,
    companies)
from app.views import dashboard_view

from app.views.template_view import (
    TemplateView,
    templates)

from app.views.company_benefit_plan_option_view import (
    CompanyBenefitPlanOptionView,
    CompanyBenefitPlansView,
    benefits
    )
from app.views.document_view import (
    CompanyUserTypeDocumentView,
    CompanyUserDocumentView,
    CompanyDocumentView,
    UserDocumentView,
    DocumentView,
    DocumentSignatureView,
    documents)
from app.views.company_templates_view import CompanyTemplatesView

from app.views.user_company_waived_benefit_view import UserCompanyWaivedBenefitView
from app.views.user_company_benefit_plan_option_view import (
    UserCompanyBenefitPlanOptionView,
    user_update_benefits)
from app.views.user_company_roles_view import UserCompanyRolesView

from app.views.w4_view import W4View
from app.views.employment_authorization_view import EmploymentAuthorizationView
from app.views.signature_view import SignatureView

from app.views.util_view import send_onboard_email

PREFIX = "api/v1"

urlpatterns = patterns('app.views',
    url(r'^dashboard/?$', dashboard_view.index, name='dashboard'),
    url(r'^%s/people/(?P<pk>[0-9]+)/?$' % PREFIX, PersonView.as_view()),

    url(r'^%s/benefit_types/?$' % PREFIX, BenefitTypeView.as_view()),

    url(r'^%s/document_types/?$' % PREFIX, DocumentTypeView.as_view()),


    url(r'^%s/users/?$' % PREFIX, UsersView.as_view()),
    url(r'^%s/users/current/?$' % PREFIX, CurrentUserView.as_view()),
    url(r'^%s/users/(?P<pk>[0-9]+)/?$' % PREFIX, UserView.as_view()),
    url(r'^%s/users/(?P<pk>[0-9]+)/family/?$' % PREFIX, UserFamilyView.as_view()),
    url(r'^%s/users/(?P<pk>[0-9]+)/documents/?$' % PREFIX, UserDocumentView.as_view()),
    url(r'^%s/users/(?P<pk>[0-9]+)/benefits/?$' % PREFIX,
        UserCompanyBenefitPlanOptionView.as_view()),
    url(r'^%s/users/(?P<pk>[0-9]+)/company_roles/?$' % PREFIX, UserCompanyRolesView.as_view()),
    url(r'^%s/users/(?P<pk>[0-9]+)/waived_benefits/?$' % PREFIX, UserCompanyWaivedBenefitView.as_view()),

    url(r'^%s/users/(?P<pk>[0-9]+)/w4/?$' % PREFIX, W4View.as_view()),
    url(r'^%s/users/(?P<pk>[0-9]+)/employment_authorization/?$' % PREFIX,
        EmploymentAuthorizationView.as_view()),
    url(r'^%s/users/(?P<pk>[0-9]+)/signature/?$' % PREFIX, SignatureView.as_view()),

    url(r'^%s/templates/(?P<pk>[0-9]+)/?$' % PREFIX, TemplateView.as_view()),
    url(r'^%s/benefits/(?P<pk>[0-9]+)/?$' % PREFIX, CompanyBenefitPlanOptionView.as_view()),

    url(r'^%s/companies/(?P<pk>[0-9]+)/benefits/?$' % PREFIX,
        CompanyBenefitPlansView.as_view()),
    url(r'^%s/companies/(?P<pk>[0-9]+)/?$' % PREFIX, CompanyView.as_view()),
    url(r'^%s/companies/(?P<pk>[0-9]+)/users/?$' % PREFIX, CompanyUserView.as_view()),
    url(r'^%s/companies/(?P<pk>[0-9]+)/documents/?$' % PREFIX, CompanyDocumentView.as_view()),
    url(r'^%s/companies/(?P<pk>[0-9]+)/templates/?$' % PREFIX, CompanyTemplatesView.as_view()),
    url(r'^%s/company_employees_count/(?P<pk>[0-9]+)/?$' % PREFIX, CompanyEmployeeCountView.as_view()),
    url(r'^%s/company_brokers_count/(?P<pk>[0-9]+)/?$' % PREFIX, CompanyBrokerCountView.as_view()),
    url(r'^%s/broker_company_count/(?P<pk>[0-9]+)/?$' % PREFIX, BrokerCompanyCountView.as_view()),

    url(r'^%s/documents/companies/(?P<pk>[0-9]+)/users/(?P<pd>[0-9]+)/?$' % PREFIX,
        CompanyUserDocumentView.as_view()),
    url(r'^%s/documents/companies/(?P<pk>[0-9]+)/users/(?P<pd>[0-9]+)/type/(?P<py>[0-9]+)/?$' % PREFIX,
        CompanyUserTypeDocumentView.as_view()),
    url(r'^%s/documents/(?P<pk>[0-9]+)/?$' % PREFIX, DocumentView.as_view()),
    url(r'^%s/documents/(?P<pk>[0-9]+)/signature/?$' % PREFIX, DocumentSignatureView.as_view()),

    url(r'^%s/benefits/?$' % PREFIX, benefits),
    url(r'^%s/companies/?$' % PREFIX, companies),
    url(r'^%s/templates/?$' % PREFIX, templates),
    url(r'^%s/documents/?$' % PREFIX, documents),
    url(r'^%s/users/(?P<pk>[0-9]+)/benefits_company=(?P<pc>[0-9]+)/?$' % PREFIX,
        user_update_benefits),


    # util api

    url(r'^%s/onboard_email/?$' % PREFIX, send_onboard_email),

)



urlpatterns = format_suffix_patterns(urlpatterns)
