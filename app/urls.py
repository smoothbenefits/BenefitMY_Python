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
    TemplateFieldView,
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

from app.views.user_company_waived_benefit_view import (
    UserCompanyWaivedBenefitView,
    CompanyWaivedBenefitView)
from app.views.user_company_benefit_plan_option_view import (
    UserCompanyBenefitPlanOptionView,
    CompanyUsersBenefitPlanOptionView)
from app.views.user_company_roles_view import UserCompanyRolesView

from app.views.w4_view import W4View
from app.views.employment_authorization_view import EmploymentAuthorizationView
from app.views.signature_view import SignatureView
from app.views.benefit_details_view import (
    BenefitDetailsView,
    delete_benefit_details)

from app.views.insurance.company_life_insurance_plan_view import \
    CompanyLifeInsurancePlanView

from app.views.insurance.user_company_life_insurance_plan_view import (
    UserCompanyLifeInsuranceView,
    CompanyUsersLifeInsuranceView)
from app.views.insurance.life_insurance_plan_view import LifeInsurancePlanView

from app.views.util_view import send_onboard_email
from app.views.user_settings_view import SettingView

from app.views.direct_deposit_view import DirectDepositView
from app.views.fsa_view import FSAView

from app.views.company_user_summary_view import (
    CompanyUsersSummaryExcelExportView,
    CompanyUsersDirectDepositExcelExportView,
    CompanyUsersLifeInsuranceBeneficiaryExcelExportView) 
from app.views.upload import (get_upload_form_policy_and_signature, 
                              UploadView)


PREFIX = "api/v1"

urlpatterns = patterns('app.views',
    url(r'^dashboard/?$', dashboard_view.index, name='dashboard'),
    url(r'^%s/people/(?P<pk>\w+)/?$' % PREFIX, PersonView.as_view(), name='people_by_id'),

    url(r'^%s/benefit_types/?$' % PREFIX, BenefitTypeView.as_view()),

    url(r'^%s/document_types/?$' % PREFIX, DocumentTypeView.as_view(), name='document_type_api'),

    url(r'^%s/users/settings/?$' % PREFIX, SettingView.as_view()),
    url(r'^%s/users/?$' % PREFIX, UsersView.as_view(), name='all_users'),
    url(r'^%s/users/current/?$' % PREFIX, CurrentUserView.as_view(), name='current_user'),
    url(r'^%s/users/(?P<pk>\w+)/?$' % PREFIX, UserView.as_view(), name='user_by_id'),
    url(r'^%s/users/(?P<pk>\w+)/family/?$' % PREFIX, UserFamilyView.as_view(), name='user_family_api'),
    url(r'^%s/users/(?P<pk>\w+)/documents/?$' % PREFIX, UserDocumentView.as_view()),
    url(r'^%s/users/(?P<pk>\w+)/benefits/?$' % PREFIX,
        UserCompanyBenefitPlanOptionView.as_view()),
    url(r'^%s/users/(?P<pk>\w+)/company_roles/?$' % PREFIX, UserCompanyRolesView.as_view(), name='user_company_api'),
    url(r'^%s/users/(?P<pk>\w+)/waived_benefits/?$' % PREFIX, UserCompanyWaivedBenefitView.as_view(), name='user_waived_benefit_api'),
    url(r'^%s/companies/(?P<pk>\w+)/waived_benefits/?$' % PREFIX, CompanyWaivedBenefitView.as_view(), name='company_waived_benefit_api'),
    url(r'^%s/users/(?P<pk>\w+)/w4/?$' % PREFIX, W4View.as_view(), name='w4_api'),
    url(r'^%s/users/(?P<pk>\w+)/employment_authorization/?$' % PREFIX,
        EmploymentAuthorizationView.as_view()),
    url(r'^%s/users/(?P<pk>\w+)/signature/?$' % PREFIX, SignatureView.as_view()),

    url(r'^%s/templates/(?P<pk>\w+)/?$' % PREFIX, TemplateView.as_view()),
    url(r'^%s/companies/(?P<pk>\w+)/template_fields/?$' % PREFIX, TemplateFieldView.as_view()),
    url(r'^%s/benefits/(?P<pk>\w+)/?$' % PREFIX, CompanyBenefitPlanOptionView.as_view(), name='benefit_plan_api'),
    url(r'^%s/benefit_details/plan=(?P<pk>\w+)/?$' % PREFIX, BenefitDetailsView.as_view()),

    url(r'^%s/benefit_details/(?P<pk>\w+)/?$' % PREFIX, delete_benefit_details),
    url(r'^%s/companies/(?P<pk>\w+)/benefits/?$' % PREFIX,
        CompanyBenefitPlansView.as_view(), name='company_benefit_plan_api'),
    url(r'^%s/company_users/(?P<pk>\w+)/benefits/?$' % PREFIX,
        CompanyUsersBenefitPlanOptionView.as_view()),

    url(r'^%s/companies/(?P<pk>\w+)/?$' % PREFIX, CompanyView.as_view()),
    url(r'^%s/companies/(?P<pk>\w+)/users/?$' % PREFIX, CompanyUserView.as_view(), name='company_users_api'),
    url(r'^%s/companies/(?P<pk>\w+)/documents/?$' % PREFIX, CompanyDocumentView.as_view()),
    url(r'^%s/companies/(?P<pk>\w+)/templates/?$' % PREFIX, CompanyTemplatesView.as_view()),
    url(r'^%s/company_employees_count/(?P<pk>\w+)/?$' % PREFIX, CompanyEmployeeCountView.as_view(), name='company_employee_count'),
    url(r'^%s/company_brokers_count/(?P<pk>\w+)/?$' % PREFIX, CompanyBrokerCountView.as_view(), name='company_broker_count'),
    url(r'^%s/broker_company_count/(?P<pk>\w+)/?$' % PREFIX, BrokerCompanyCountView.as_view(), name='broker_company_count'),
    url(r'^%s/companies/(?P<pk>\w+)/users/excel/?$' % PREFIX, CompanyUsersSummaryExcelExportView.as_view()),
    url(r'^%s/companies/(?P<pk>\w+)/users/excel/life_beneficiary?$' % PREFIX, CompanyUsersLifeInsuranceBeneficiaryExcelExportView.as_view()),
    url(r'^%s/companies/(?P<pk>\w+)/users/excel/direct_deposit?$' % PREFIX, CompanyUsersDirectDepositExcelExportView.as_view()),

    url(r'^%s/documents/companies/(?P<pk>\w+)/users/(?P<pd>\w+)/?$' % PREFIX,
        CompanyUserDocumentView.as_view()),
    url(r'^%s/documents/companies/(?P<pk>\w+)/users/(?P<pd>\w+)/type/(?P<py>\w+)/?$' % PREFIX,
        CompanyUserTypeDocumentView.as_view()),
    url(r'^%s/documents/(?P<pk>\w+)/?$' % PREFIX, DocumentView.as_view()),
    url(r'^%s/documents/(?P<pk>\w+)/signature/?$' % PREFIX, DocumentSignatureView.as_view()),

    url(r'^%s/fsa/(?P<pk>\w+)/?$' % PREFIX, FSAView.as_view(), name='fsa_api'),
    url(r'^%s/direct_deposit/(?P<pk>\w+)/?$' % PREFIX, DirectDepositView.as_view(), name='direct_deposit_api'),
    url(r'^%s/benefits/?$' % PREFIX, benefits),
    url(r'^%s/companies/?$' % PREFIX, companies),
    url(r'^%s/templates/?$' % PREFIX, templates),
    url(r'^%s/documents/?$' % PREFIX, documents),


    url(r'^%s/brokers/(?P<pk>\w+)/life_insurance_plan/?$' % PREFIX,
        LifeInsurancePlanView.as_view(), name='broker_life_insurance_api'),


    url(r'^%s/users/(?P<pk>\w+)/life_insurance/?$' % PREFIX,
        UserCompanyLifeInsuranceView.as_view(), name='user_life_insurance_api'),

    url(r'^%s/company_users/(?P<pk>\w+)/life_insurance/?$' % PREFIX,
        CompanyUsersLifeInsuranceView.as_view(), name='company_users_life_insurance_api'),

    url(r'^%s/company/(?P<pk>\w+)/life_insurance_plan/?$' % PREFIX,
        CompanyLifeInsurancePlanView.as_view(), name='company_life_insurance_plan_api'),

    # util api

    url(r'^%s/onboard_email/?$' % PREFIX, send_onboard_email),

    # upload API
    url(r'^%s/companies/(?P<pk>\w+)/upload/meta/(?P<user_id>\w+)/?$' % PREFIX, 
        get_upload_form_policy_and_signature, 
        name='get_upload_policy_signature'),
)



urlpatterns = format_suffix_patterns(urlpatterns)
