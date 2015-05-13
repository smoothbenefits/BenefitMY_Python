from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns


from app.views.person_view import (
    PersonView, FamilyByUserView)
from app.views.employee_profile_view import (
    EmployeeProfileView,
    EmployeeProfileByPersonCompanyView,
    EmployeeProfileByCompanyUserView)
from app.views.user_view import (
    UserView,
    UsersView,
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


from app.views.insurance.company_std_insurance_plan_view import \
    CompanyStdInsurancePlanView

from app.views.insurance.user_company_std_insurance_plan_view import (
    UserCompanyStdInsuranceView,
    CompanyUsersStdInsuranceView)
from app.views.insurance.std_insurance_plan_view import StdInsurancePlanView

from app.views.insurance.company_ltd_insurance_plan_view import \
    CompanyLtdInsurancePlanView
from app.views.insurance.user_company_ltd_insurance_plan_view import (
    UserCompanyLtdInsuranceView,
    CompanyUsersLtdInsuranceView)
from app.views.insurance.ltd_insurance_plan_view import LtdInsurancePlanView

from app.views.insurance.company_supplemental_life_insurance_plan_view import (
    CompanySupplementalLifeInsurancePlanView, 
    CompanySupplementalLifeInsurancePlanByCompanyView)
from app.views.insurance.person_company_supplemental_life_insurance_plan_view import (
    PersonCompanySupplementalLifeInsurancePlanView,
    CompanyPersonsSupplementalLifeInsuranceView,
    PersonSupplementalLifeInsuranceByPersonView)
from app.views.insurance.supplemental_life_insurance_plan_view import \
    SupplementalLifeInsurancePlanView
from app.views.sys_suppl_life_insurance_condition_view import SysSupplementalLifeInsuranceConditionView

from app.views.util_view import send_onboard_email
from app.views.user_settings_view import SettingView

from app.views.direct_deposit_view import DirectDepositView
from app.views.company_features_view import CompanyFeaturesView
from app.views.sys_application_feature_view import SysApplicationFeatureView

from app.views.fsa.fsa_view import (
    FsaView,
    FSAByUserView)
from app.views.fsa.company_fsa_plan_view import (
    CompanyFsaPlanView,
    CompanyFsaPlanByCompanyView)
from app.views.fsa.fsa_plan_view import FsaPlanView

from app.views.company_user_summary_view import (
    CompanyUsersSummaryExcelExportView,
    CompanyUsersDirectDepositExcelExportView,
    CompanyUsersLifeInsuranceBeneficiaryExcelExportView)

from app.views.upload import (UserUploadView,
                              UploadView,
                              get_company_uploads)
from app.views.upload_application_feature_view import UploadApplicationFeatureView
from app.views.upload_audience_view import UploadAudienceByCompanyView

from app.views.data_modification.company_user_data_modification import CompanyUsersDataModificationSummaryView

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
    url(r'^%s/users/(?P<pk>\w+)/family/?$' % PREFIX, FamilyByUserView.as_view(), name='user_family_api'),
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

    url(r'^%s/companies/(?P<pk>\w+)/users/modification_summary/?$' % PREFIX, CompanyUsersDataModificationSummaryView.as_view()),

    url(r'^%s/documents/companies/(?P<pk>\w+)/users/(?P<pd>\w+)/?$' % PREFIX,
        CompanyUserDocumentView.as_view()),
    url(r'^%s/documents/companies/(?P<pk>\w+)/users/(?P<pd>\w+)/type/(?P<py>\w+)/?$' % PREFIX,
        CompanyUserTypeDocumentView.as_view()),
    url(r'^%s/documents/(?P<pk>\w+)/?$' % PREFIX, DocumentView.as_view()),
    url(r'^%s/documents/(?P<pk>\w+)/signature/?$' % PREFIX, DocumentSignatureView.as_view()),

    url(r'^%s/direct_deposit/(?P<pk>\w+)/?$' % PREFIX, DirectDepositView.as_view(), name='direct_deposit_api'),
    url(r'^%s/company_features/(?P<pk>\w+)/?$' % PREFIX, CompanyFeaturesView.as_view(), name='company_features_api'),
    url(r'^%s/application_features/?$' % PREFIX, SysApplicationFeatureView.as_view(), name='sys_application_feature_api'),
    url(r'^%s/benefits/?$' % PREFIX, benefits),
    url(r'^%s/companies/?$' % PREFIX, companies),
    url(r'^%s/templates/?$' % PREFIX, templates),
    url(r'^%s/documents/?$' % PREFIX, documents),

    # FSA api
    url(r'^%s/brokers/(?P<pk>\w+)/fsa/?$' % PREFIX, 
        FsaPlanView.as_view(), name='broker_fsa_api'),

    url(r'^%s/company_users/(?P<pk>\w+)/fsa/?$' % PREFIX,
        FsaView.as_view(), name='company_users_fsa_api'),

    url(r'^%s/user_company/(?P<user_id>\w+)/fsa/?$' % PREFIX,
        FSAByUserView.as_view(), name='user_company_fsa_api'),

    url(r'^%s/broker_company/(?P<pk>\w+)/fsa/?$' % PREFIX,
        CompanyFsaPlanView.as_view(), name='broker_company_fsa_api'),

    url(r'^%s/company/(?P<pk>\w+)/fsa/?$' % PREFIX,
        CompanyFsaPlanByCompanyView.as_view(), name='company_fsa_api'),

    # Life insurance api
    url(r'^%s/brokers/(?P<pk>\w+)/life_insurance_plan/?$' % PREFIX,
        LifeInsurancePlanView.as_view(), name='broker_life_insurance_api'),

    url(r'^%s/users/(?P<pk>\w+)/life_insurance/?$' % PREFIX,
        UserCompanyLifeInsuranceView.as_view(), name='user_life_insurance_api'),

    url(r'^%s/company_users/(?P<pk>\w+)/life_insurance/?$' % PREFIX,
        CompanyUsersLifeInsuranceView.as_view(), name='company_users_life_insurance_api'),

    url(r'^%s/company/(?P<pk>\w+)/life_insurance_plan/?$' % PREFIX,
        CompanyLifeInsurancePlanView.as_view(), name='company_life_insurance_plan_api'),

    # Supplemental life insurance api
    url(r'^%s/supplemental_life_condition/?$' % PREFIX,
        SysSupplementalLifeInsuranceConditionView.as_view(), name='suppl_life_condition'),

    url(r'^%s/supplemental_life/(?P<pk>\w+)/?$' % PREFIX,
        SupplementalLifeInsurancePlanView.as_view(), name='suppl_life_api'),

    url(r'^%s/company_suppl_life/(?P<pk>\w+)/?$' % PREFIX,
        CompanySupplementalLifeInsurancePlanView.as_view(), name='comp_suppl_life_api'),

    url(r'^%s/company/(?P<company_id>\w+)/company_suppl_life/?$' % PREFIX,
        CompanySupplementalLifeInsurancePlanByCompanyView.as_view(), name='company_comp_suppl_life'),

    url(r'^%s/person_comp_suppl_life/(?P<pk>\w+)/?$' % PREFIX,
        PersonCompanySupplementalLifeInsurancePlanView.as_view(), name='person_suppl_life_api'),

    url(r'^%s/company/(?P<company_id>\w+)/person_comp_suppl_life/?$' % PREFIX,
        CompanyPersonsSupplementalLifeInsuranceView.as_view(), name='company_person_supple_life'),

    url(r'^%s/person/(?P<person_id>\w+)/person_comp_suppl_life/?$' % PREFIX,
        PersonSupplementalLifeInsuranceByPersonView.as_view(), name='person_person_supple_life'),

    # STD insurance api
    url(r'^%s/brokers/(?P<pk>\w+)/std_insurance_plan/?$' % PREFIX,
        StdInsurancePlanView.as_view(), name='broker_std_insurance_api'),

    url(r'^%s/users/(?P<pk>\w+)/std_insurance/?$' % PREFIX,
        UserCompanyStdInsuranceView.as_view(), name='user_std_insurance_api'),

    url(r'^%s/company_users/(?P<pk>\w+)/std_insurance/?$' % PREFIX,
        CompanyUsersStdInsuranceView.as_view(), name='company_users_std_insurance_api'),

    url(r'^%s/company/(?P<pk>\w+)/std_insurance_plan/?$' % PREFIX,
        CompanyStdInsurancePlanView.as_view(), name='company_std_insurance_plan_api'),

    # LTD insurance api
    url(r'^%s/brokers/(?P<pk>\w+)/ltd_insurance_plan/?$' % PREFIX,
        LtdInsurancePlanView.as_view(), name='broker_ltd_insurance_api'),

    url(r'^%s/users/(?P<pk>\w+)/ltd_insurance/?$' % PREFIX,
        UserCompanyLtdInsuranceView.as_view(), name='user_ltd_insurance_api'),

    url(r'^%s/company_users/(?P<pk>\w+)/ltd_insurance/?$' % PREFIX,
        CompanyUsersLtdInsuranceView.as_view(), name='company_users_ltd_insurance_api'),

    url(r'^%s/company/(?P<pk>\w+)/ltd_insurance_plan/?$' % PREFIX,
        CompanyLtdInsurancePlanView.as_view(), name='company_ltd_insurance_plan_api'),

    # util api

    url(r'^%s/onboard_email/?$' % PREFIX, send_onboard_email),

    # upload API
    url(r'^%s/users/(?P<pk>\w+)/uploads/?$' % PREFIX,
        UserUploadView.as_view(),
        name='uploads_by_user'),
    # GET and POST

    # GET PUT and DELETE
    url(r'^%s/upload/(?P<pk>\w+)/?$' % PREFIX,
        UploadView.as_view(),
        name='upload_api'),

    url(r'^%s/companies/(?P<comp_id>\w+)/uploads/(?P<pk>\w+)/?$' % PREFIX,
        get_company_uploads,
        name='get_comp_uploads'),
    url(r'^%s/upload/application_features/(?P<pk>\w+)/(?P<feature_id>\w+)/?$' % PREFIX,
        UploadApplicationFeatureView.as_view(),
        name='uploads_application_feature_api'),
    url(r'^%s/upload/audience/(?P<comp_id>\w+)/?$' % PREFIX,
        UploadAudienceByCompanyView.as_view(),
        name='upload_audience_api'),

    url(r'^%s/employee_profile/(?P<pk>\w+)/?$' % PREFIX,
        EmployeeProfileView.as_view(),
        name='employee_profile_api'),
    url(r'^%s/person/(?P<person_id>\w+)/company/(?P<company_id>\w+)/employee_profile/?$' % PREFIX,
        EmployeeProfileByPersonCompanyView.as_view(),
        name='employee_profile_by_person_company_api'),
    url(r'^%s/company/(?P<company_id>\w+)/user/(?P<user_id>\w+)/employee_profile/?$' % PREFIX,
        EmployeeProfileByCompanyUserView.as_view(),
        name='employee_profile_by_company_user_api'),
)



urlpatterns = format_suffix_patterns(urlpatterns)
