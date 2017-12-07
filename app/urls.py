from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

from app.views.person_view import (
    PersonView, FamilyByUserView)
from app.views.employee_profile_view import (
    EmployeeProfileView,
    EmployeeProfileByPersonCompanyView,
    EmployeeProfileByCompanyUserView,
    EmployeeProfilesByCompanyView,
    EmployeeProfileByCompanyPinView)
from app.views.employee_compensation_view import (
    EmployeeCompensationView,
    EmployeeCompensationByPersonView)
from app.views.employee_timetracking_view import (
    EmployeeTimeTrackingView,
    EmployeeTimeTrackingByPersonCompanyView)
from app.views.user_view import (
    UserView,
    UsersView,
    CurrentUserView,
    UserCredentialView,
    UserByCredentialView)
from app.views.company_user_view import (
    CompanyUserView,
    CompanyEmployeeCountView,
    BrokerCompanyCountView,
    CompanyBrokerCountView,
    CompanyUserDetailView)
from app.views.health_benefits.benefit_policy_key_view import BenefitPolicyKeyView
from app.views.health_benefits.benefit_type_view import BenefitTypeView
from app.views.document_type_view import DocumentTypeView
from app.views.company_view import (
    CompanyView)
from app.views import dashboard_view

from app.views.template_view import (
    TemplateView,
    TemplateFieldView,
    templates)

from app.views.health_benefits.benefit_plan_view import (
    BenefitPlanView, BenefitPlanCreationView)

from app.views.health_benefits.company_benefit_plan_option_view import (
    CompanyBenefitPlanOptionView,
    CompanyBenefitPlansView,
    create_benefit_plan_option)
from app.views.health_benefits.company_group_benefit_plan_option_view import (
    CompanyGroupBenefitPlanOptionByCompanyGroupView,
    CompanyGroupBenefitPlanOptionByCompanyPlanView)

from app.views.document_view import (
    CompanyUserTypeDocumentView,
    CompanyUserDocumentView,
    CompanyDocumentView,
    UserDocumentView,
    DocumentView,
    DocumentSignatureView,
    DocumentDownloadView,
    documents)
from app.views.company_templates_view import CompanyTemplatesView

from app.views.health_benefits.user_company_waived_benefit_view import (
    UserCompanyWaivedBenefitView,
    CompanyWaivedBenefitView)
from app.views.health_benefits.user_company_benefit_plan_option_view import (
    UserCompanyBenefitPlanOptionView,
    CompanyUsersBenefitPlanOptionView)
from app.views.user_company_roles_view import UserCompanyRolesView

from app.views.w4_view import W4View
from app.views.tax.employee_state_tax_election_view import (
    EmployeeStateTaxElectionView,
    EmployeeStateTaxElectionByEmployeeView
)
from app.views.employment_authorization_view import EmploymentAuthorizationView
from app.views.signature_view import (SignatureByUserView, SignatureView)
from app.views.health_benefits.benefit_details_view import (
    BenefitDetailsView,
    delete_benefit_details)
from app.views.open_enrollment_definition_view import OpenEnrollmentDefinitionByCompanyView

#Basic Life
from app.views.insurance.company_life_insurance_plan_view import \
    CompanyLifeInsurancePlanView
from app.views.insurance.company_group_basic_life_insurance_plan_view import (
    CompanyGroupBasicLifeInsurancePlanByCompanyGroupView,
    CompanyGroupBasicLifeInsurancePlanByCompanyPlanView
)
from app.views.insurance.user_company_life_insurance_plan_view import (
    UserCompanyLifeInsuranceView,
    CompanyUsersLifeInsuranceView)
from app.views.insurance.life_insurance_plan_view import LifeInsurancePlanView

#STD
from app.views.insurance.company_std_insurance_plan_view import \
    CompanyStdInsurancePlanView
from app.views.insurance.user_company_std_insurance_plan_view import (
    UserCompanyStdInsuranceView,
    CompanyUsersStdInsuranceView)
from app.views.insurance.std_insurance_plan_view import StdInsurancePlanView
from app.views.insurance.company_group_std_insurance_plan_view import (
    CompanyGroupStdInsurancePlanByCompanyGroupView,
    CompanyGroupStdInsurancePlanByCompanyPlanView
)

#LTD
from app.views.insurance.company_ltd_insurance_plan_view import \
    CompanyLtdInsurancePlanView
from app.views.insurance.user_company_ltd_insurance_plan_view import (
    UserCompanyLtdInsuranceView,
    CompanyUsersLtdInsuranceView)
from app.views.insurance.ltd_insurance_plan_view import LtdInsurancePlanView
from app.views.insurance.company_group_ltd_insurance_plan_view import (
    CompanyGroupLtdInsurancePlanByCompanyGroupView,
    CompanyGroupLtdInsurancePlanByCompanyPlanView
)

#Supplemental Life
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
from app.views.insurance.company_group_supplemental_life_insurance_plan_view import (
    CompanyGroupSupplementalLifeInsurancePlanByCompanyGroupView,
    CompanyGroupSupplementalLifeInsurancePlanByCompanyPlanView)

#HRA
from app.views.hra.hra_plan_view import HraPlanView
from app.views.hra.company_hra_plan_view import (
    CompanyHraPlanView,
    CompanyHraPlanByCompanyView)
from app.views.hra.person_company_hra_plan_view import (
    PersonCompanyHraPlanView,
    PersonCompanyHraPlanByPersonView)
from app.views.hra.company_group_hra_plan_view import (
    CompanyGroupHraPlanByCompanyGroupView,
    CompanyGroupHraPlanByCompanyPlanView)

#Commuter
from app.views.commuter.company_commuter_plan_view import (
    CompanyCommuterPlanView,
    CompanyCommuterPlanByCompanyView)
from app.views.commuter.person_company_commuter_plan_view import (
    PersonCompanyCommuterPlanView,
    PersonCompanyCommuterPlanByPersonView)
from app.views.commuter.company_group_commuter_plan_view import (
    CompanyGroupCommuterPlanByCompanyGroupView,
    CompanyGroupCommuterPlanByCompanyPlanView)

#Extra Benefits
from app.views.extra_benefits.company_extra_benefit_plan_view import (
    CompanyExtraBenefitPlanView,
    CompanyExtraBenefitPlanByCompanyView)
from app.views.extra_benefits.person_company_extra_benefit_plan_view import (
    PersonCompanyExtraBenefitPlanView,
    PersonCompanyExtraBenefitPlanByPersonView)

from app.views.util_view import send_onboard_email
from app.views.user_settings_view import SettingView

from app.views.direct_deposit_view import DirectDepositView
from app.views.company_features_view import (
    CompanyFeaturesView,
    CompleteCompanyApplicationFeaturesView)
from app.views.company_user_features_view import \
    CompleteCompanyUserApplicationFeaturesView
from app.views.company_group_view import CompanyGroupView
from app.views.company_group_member_view import (
    CompanyGroupMemberView,
    CompanyGroupMemberCompanyGroupView,
    CompanyGroupMemberCompanyView)
from app.views.sys_application_feature_view import SysApplicationFeatureView

from app.views.fsa.fsa_view import (
    FsaView,
    FSAByUserView)
from app.views.fsa.company_fsa_plan_view import (
    CompanyFsaPlanView,
    CompanyFsaPlanByCompanyView)
from app.views.fsa.fsa_plan_view import FsaPlanView
from app.views.fsa.company_group_fsa_plan_view import (
    CompanyGroupFsaPlanByCompanyGroupView,
    CompanyGroupFsaPlanByCompanyPlanView)

from app.views.hsa.company_group_hsa_plan_view import (
    CompanyGroupHsaPlanByCompanyGroupView, CompanyGroupHsaPlanByCompanyPlanView)
from app.views.hsa.company_hsa_plan_view import CompanyHsaPlanView, CompanyHsaPlanByCompanyView
from app.views.hsa.person_company_group_hsa_plan_view import (
    PersonCompanyGroupHsaPlanView, PersonCompanyGroupHsaPlanByPersonView)

from app.views.reports.company_users_full_summary_excel import CompanyUsersFullSummaryExcelExportView
from app.views.reports.company_users_benefits_billing_excel import CompanyUsersBenefitsBillingExcelExportView
from app.views.reports.company_users_direct_deposit_excel import CompanyUsersDirectDepositExcelExportView
from app.views.reports.company_users_life_insurance_beneficiary_excel import CompanyUsersLifeInsuranceBeneficiaryExcelExportView
from app.views.reports.company_users_worktime_report import CompanyUsersWorktimeWeeklyReportView
from app.views.reports.company_users_time_punch_card_report import CompanyUsersTimePunchCardWeeklyReportView
from app.views.reports.company_users_time_punch_card_report_v2 import CompanyUsersTimePunchCardWeeklyReportV2View
from app.views.reports.time_tracking.company_time_off_report_csv import CompanyTimeOffReportCsvView

from app.views.reports.company_users_summary_pdf import CompanyUsersSummaryPdfExportView

from app.views.reports.integration.company_hphc_excel import CompanyHphcExcelView

from app.views.reports.forms.form_1095c import Form1095CView
from app.views.reports.forms.form_1094c import Form1094CView
from app.views.reports.forms.COI.form_lien_waiver import FormLienWaiverView
from app.views.reports.forms.form_i9 import FormI9View
from app.views.reports.forms.form_w4 import FormW4View

from app.views.upload import (UserUploadView,
                              UploadView,
                              get_company_uploads)
from app.views.upload_application_feature_view import UploadApplicationFeatureView
from app.views.upload_for_user_view import UploadForUserView

from app.views.data_modification.company_user_data_modification import CompanyUsersDataModificationSummaryView

from app.views.sys_benefit_update_reason_view import SysBenefitUpdateReasonView

from app.views.person_enrollment_summary_view import PersonEnrollmentSummaryView
from app.views.company_benefit_availability_view import CompanyBenefitAvailabilityView
from app.views.sys_period_definition_view import SysPeriodDefinitionView
from app.views.insurance.company_life_insurance_employee_premium_view import CompanyLifeInsuranceEmployeePremiumView
from app.views.insurance.company_ltd_insurance_employee_premium_view import CompanyLtdInsuranceEmployeePremiumView
from app.views.insurance.company_std_insurance_employee_premium_view import CompanyStdInsuranceEmployeePremiumView
from app.views.company_enrollment_summary_view import CompanyEnrollmentSummaryView
from app.views.aca.company_1095_c_view import Company1095CView
from app.views.aca.employee_1095_c_view import Employee1095CView
from app.views.aca.aca_1095_c_periods_view import ACA1095CPeriodsView
from app.views.aca.company_1094_c_view import Company1094CView
from app.views.aca.aca_1094_c_eligibility_certification_view import ACA1094CEligibilityCertificationView

from app.views.batch_account_creation.batch_account_creation_view import BatchAccountCreationView
from app.views.batch_account_creation.account_info_list_parse_view import AccountInfoListParseView

from app.views.employee_organization.batch_employee_organization_import_raw_data_parse_view \
    import BatchEmployeeOrganizationImportRawDataParseView
from app.views.employee_organization.batch_employee_organization_import_view \
    import BatchEmployeeOrganizationImportView

from app.views.employee_management.employee_termination_view import EmployeeTerminationView
from app.views.employee_management.reporting_structure_view import DirectReportsView, DirectReportCountView

from app.views.user_data_change_email_view import UserDataChangeEmailView

from app.views.logging_service_view import LoggingServiceView

# Onboarding
from app.views.onboarding.user_onboarding_step_state_view import (
    UserOnboardingStepStateView,
    UserOnboardingStepStateByUserView
)

# Company Service provider_type
from app.views.company_service_provider_view import (
    CompanyServiceProviderView,
    CompanyServiceProviderByCompanyView
)

# Workers' Comp
from app.views.workers_comp.phraseology_view import \
    AllPhraseologyView
from app.views.workers_comp.company_phraseology_view import (
    CompanyPhraseologyView,
    CompanyPhraseologyByCompanyView)
from app.views.workers_comp.employee_phraseology_view import (
    EmployeePhraseologyView,
    EmployeePhraseologyByEmployeePersonView)

# Company Metadata
from app.views.company_department_view import (
    CompanyDepartmentView,
    CompanyDepartmentByCompanyView)
from app.views.company_job_view import (
    CompanyJobView,
    CompanyJobByCompanyView)
from app.views.company_division_view import (
    CompanyDivisionView,
    CompanyDivisionByCompanyView)

# Integrations

# # Common
from app.views.integration.company_integration_provider_view import CompanyIntegrationProvidersByCompanyView

# # Advatage Payroll
from app.views.reports.integration.advantage_payroll.advantage_payroll_client_setup_csv \
    import AdvantagePayrollClientSetupCsvView
from app.views.reports.integration.advantage_payroll.advantage_payroll_period_export_csv \
    import AdvantagePayrollPeriodExportCsvView

# # Connect Payroll
from app.views.reports.integration.connect_payroll.connect_payroll_period_export_csv \
    import ConnectPayrollPeriodExportCsvView
from app.views.reports.integration.connect_payroll.connect_payroll_employee_front_page_csv \
    import ConnectPayrollEmployeeFrontPageCsvView

from app.views.admin.password_generator_view import PasswordGeneratorView
from app.views.admin.ssn_format_correction_view import SsnFormatCorrectionForAllView

PREFIX = "api/v1"
PREFIX_V2 = "api/v2"
ADMIN_PREFIX = 'admin/v1'

urlpatterns = patterns('app.views',
    url(r'^dashboard/?$', dashboard_view.index, name='dashboard'),
    url(r'^%s/people/(?P<pk>\w+)/?$' % PREFIX, PersonView.as_view(), name='people_by_id'),

    url(r'^%s/benefit_types/?$' % PREFIX, BenefitTypeView.as_view()),

    url(r'^%s/document_types/?$' % PREFIX, DocumentTypeView.as_view(), name='document_type_api'),

    url(r'^%s/users/settings/?$' % PREFIX, SettingView.as_view()),
    url(r'^%s/users/?$' % PREFIX, UsersView.as_view(), name='all_users'),
    url(r'^%s/users/current/?$' % PREFIX, CurrentUserView.as_view(), name='current_user'),
    url(r'^%s/users/credential/?$' % PREFIX, UserCredentialView.as_view(), name='user_credential'),
    url(r'^%s/user/auth/?$' % PREFIX, UserByCredentialView.as_view(), name='user_by_credential'),
    url(r'^%s/users/(?P<pk>\w+)/?$' % PREFIX, UserView.as_view(), name='user_by_id'),
    url(r'^%s/users/(?P<pk>\w+)/family/?$' % PREFIX, FamilyByUserView.as_view(), name='user_family_api'),
    url(r'^%s/users/(?P<pk>\w+)/documents/?$' % PREFIX, UserDocumentView.as_view()),
    url(r'^%s/users/(?P<pk>\w+)/benefits/?$' % PREFIX,
        UserCompanyBenefitPlanOptionView.as_view()),
    url(r'^%s/users/(?P<pk>\w+)/company_roles/?$' % PREFIX, UserCompanyRolesView.as_view(), name='user_company_api'),
    url(r'^%s/users/(?P<pk>\w+)/waived_benefits/?$' % PREFIX, UserCompanyWaivedBenefitView.as_view(), name='user_waived_benefit_api'),
    url(r'^%s/companies/(?P<pk>\w+)/waived_benefits/?$' % PREFIX, CompanyWaivedBenefitView.as_view(), name='company_waived_benefit_api'),
    url(r'^%s/users/(?P<pk>\w+)/w4/?$' % PREFIX, W4View.as_view(), name='w4_api'),
    url(r'^%s/users/(?P<user_id>\w+)/w4/states/(?P<state>\w+)/?$' % PREFIX, EmployeeStateTaxElectionView.as_view(), name='employee_state_tax_election_api'),
    url(r'^%s/users/(?P<user_id>\w+)/w4/states/?$' % PREFIX, EmployeeStateTaxElectionByEmployeeView.as_view(), name='employee_state_tax_election_by_employee_api'),
    url(r'^%s/users/(?P<pk>\w+)/employment_authorization/?$' % PREFIX,
        EmploymentAuthorizationView.as_view()),
    url(r'^%s/signature/?$' % PREFIX, SignatureView.as_view()),
    url(r'^%s/signature/(?P<pk>\w+)/?$' % PREFIX, SignatureView.as_view()),
    url(r'^%s/users/(?P<user_id>\w+)/signature/?$' % PREFIX, SignatureByUserView.as_view()),

    url(r'^%s/templates/(?P<pk>\w+)/?$' % PREFIX, TemplateView.as_view()),
    url(r'^%s/companies/(?P<pk>\w+)/template_fields/?$' % PREFIX, TemplateFieldView.as_view()),
    url(r'^%s/benefits/(?P<pk>\w+)/?$' % PREFIX, BenefitPlanView.as_view(), name='benefit_plan_api'),
    url(r'^%s/benefit_policy_keys/?$' % PREFIX, BenefitPolicyKeyView.as_view(), name='benefit_policy_key_api'),
    url(r'^%s/benefit_options/?$' % PREFIX, create_benefit_plan_option, name='company_benefit_post_api'),
    url(r'^%s/benefit_details/plan=(?P<pk>\w+)/?$' % PREFIX, BenefitDetailsView.as_view()),

    url(r'^%s/benefit_details/(?P<pk>\w+)/?$' % PREFIX, delete_benefit_details),
    url(r'^%s/companies/(?P<pk>\w+)/benefits/?$' % PREFIX,
        CompanyBenefitPlansView.as_view(), name='company_benefit_plan_api'),
    url(r'^%s/company_users/(?P<pk>\w+)/benefits/?$' % PREFIX,
        CompanyUsersBenefitPlanOptionView.as_view()),

    url(r'^%s/company_group/(?P<company_group_id>\w+)/health_benefits/?$' % PREFIX,
        CompanyGroupBenefitPlanOptionByCompanyGroupView.as_view(),
        name='company_group_benefit_plan_option_api'),
    url(r'^%s/company_health_benefits/(?P<pk>\w+)/company_group_plans/?$' % PREFIX,
        CompanyGroupBenefitPlanOptionByCompanyPlanView.as_view(),
        name='company_group_benefit_plan_option_by_company_plan_api'),

    url(r'^%s/companies/(?P<pk>\w+)/?$' % PREFIX, CompanyView.as_view()),
    url(r'^%s/companies/?$' % PREFIX, CompanyView.as_view()),
    url(r'^%s/companies/(?P<pk>\w+)/users/?$' % PREFIX, CompanyUserView.as_view(), name='company_users_api'),
    url(r'^%s/companies/(?P<comp_id>\w+)/users/(?P<user_id>\w+)/direct_reports/?$' % PREFIX, DirectReportsView.as_view(), name='direct_reports_api'),
    url(r'^%s/companies/(?P<comp_id>\w+)/users/(?P<user_id>\w+)/direct_report_count/?$' % PREFIX, DirectReportCountView.as_view(), name='direct_report_count_api'),
    url(r'^%s/companies/(?P<pk>\w+)/documents/?$' % PREFIX, CompanyDocumentView.as_view()),
    url(r'^%s/companies/(?P<pk>\w+)/templates/?$' % PREFIX, CompanyTemplatesView.as_view()),
    url(r'^%s/company_employees_count/(?P<pk>\w+)/?$' % PREFIX, CompanyEmployeeCountView.as_view(), name='company_employee_count'),
    url(r'^%s/company_brokers_count/(?P<pk>\w+)/?$' % PREFIX, CompanyBrokerCountView.as_view(), name='company_broker_count'),
    url(r'^%s/broker_company_count/(?P<pk>\w+)/?$' % PREFIX, BrokerCompanyCountView.as_view(), name='broker_company_count'),
    url(r'^%s/companies/(?P<pk>\w+)/users/excel/?$' % PREFIX, CompanyUsersFullSummaryExcelExportView.as_view(), name='company_full_summary_excel_api'),
    url(r'^%s/companies/(?P<pk>\w+)/users/excel/life_beneficiary?$' % PREFIX, CompanyUsersLifeInsuranceBeneficiaryExcelExportView.as_view(), name='company_life_insurance_beneficiary_excel_api'),
    url(r'^%s/companies/(?P<pk>\w+)/users/excel/direct_deposit?$' % PREFIX, CompanyUsersDirectDepositExcelExportView.as_view(), name='company_direct_deposit_excel_api'),
    url(r'^%s/companies/(?P<pk>\w+)/users/excel/benefits_billing?$' % PREFIX, CompanyUsersBenefitsBillingExcelExportView.as_view()),
    url(r'^%s/company/(?P<pk>\w+)/worktime_excel/from/(?P<from_year>\d+)/(?P<from_month>\d+)/(?P<from_day>\d+)/to/(?P<to_year>\d+)/(?P<to_month>\d+)/(?P<to_day>\d+)/?$' % PREFIX,
        CompanyUsersWorktimeWeeklyReportView.as_view(), name='company_worktime_report_weekly'),
    url(r'^%s/companies/(?P<pk>\w+)/time_punch_card_excel/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/?$' % PREFIX,
        CompanyUsersTimePunchCardWeeklyReportView.as_view(), name='company_time_punch_card_report_weekly'),
    url(r'^%s/companies/(?P<pk>\w+)/time_punch_card_excel/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/?$' % PREFIX_V2,
        CompanyUsersTimePunchCardWeeklyReportV2View.as_view(), name='company_time_punch_card_report_weekly_v2'),
    url(r'^%s/companies/(?P<company_id>\w+)/time_off_report_csv/from/(?P<from_year>\d+)/(?P<from_month>\d+)/(?P<from_day>\d+)/to/(?P<to_year>\d+)/(?P<to_month>\d+)/(?P<to_day>\d+)/?$' % PREFIX,
        CompanyTimeOffReportCsvView.as_view(), name='company_time_off_report_csv'),

    url(r'^%s/companies/(?P<pk>\w+)/users/pdf/?$' % PREFIX, CompanyUsersSummaryPdfExportView.as_view(), name='company_summary_pdf_api'),
    url(r'^%s/company/(?P<pk>\w+)/role/(?P<role_type>\w+)/?$' % PREFIX, CompanyUserDetailView.as_view(), name='company_user_details_api'),

    url(r'^%s/companies/(?P<pk>\w+)/hphc/excel/?$' % PREFIX, CompanyHphcExcelView.as_view(), name='company_hphc_excel_api'),
    url(r'^%s/companies/(?P<comp_id>\w+)/open_enrollment/?$' % PREFIX, OpenEnrollmentDefinitionByCompanyView.as_view(), name='company_open_enrollment_api'),
    url(r'^%s/users/(?P<pk>\w+)/forms/1095c/?$' % PREFIX, Form1095CView.as_view(), name='employee_1095_c_form_api'),
    url(r'^%s/company/(?P<pk>\w+)/forms/1094c/?$' % PREFIX, Form1094CView.as_view(), name='company_1094_c_form_api'),

    url(r'^%s/users/(?P<pk>\w+)/forms/i9/?$' % PREFIX, FormI9View.as_view(), name='employee_i9_form_api'),
    url(r'^%s/users/(?P<pk>\w+)/forms/w4/?$' % PREFIX, FormW4View.as_view(), name='employee_w4_form_api'),

    url(r'^%s/company/(?P<company_id>\w+)/contractors/(?P<contractor_id>\w+)/forms/lien_waiver/?$' % PREFIX, FormLienWaiverView.as_view(), name='coi_lien_waiver_form_api'),

    url(r'^%s/companies/(?P<pk>\w+)/users/modification_summary/?$' % PREFIX, CompanyUsersDataModificationSummaryView.as_view()),

    url(r'^%s/documents/companies/(?P<pk>\w+)/users/(?P<pd>\w+)/?$' % PREFIX,
        CompanyUserDocumentView.as_view()),
    url(r'^%s/documents/companies/(?P<pk>\w+)/users/(?P<pd>\w+)/type/(?P<py>\w+)/?$' % PREFIX,
        CompanyUserTypeDocumentView.as_view()),
    url(r'^%s/documents/(?P<pk>\w+)/?$' % PREFIX, DocumentView.as_view()),
    url(r'^%s/documents/(?P<pk>\w+)/signature/?$' % PREFIX, DocumentSignatureView.as_view()),

    url(r'^%s/documents/(?P<document_id>\w+)/download/?$' % PREFIX, DocumentDownloadView.as_view()),

    url(r'^%s/direct_deposit/(?P<pk>\w+)/?$' % PREFIX, DirectDepositView.as_view(), name='direct_deposit_api'),
    url(r'^%s/application_features/?$' % PREFIX, SysApplicationFeatureView.as_view(), name='sys_application_feature_api'),
    url(r'^%s/period_definitions/?$' % PREFIX, SysPeriodDefinitionView.as_view(), name='sys_period_definition_api'),
    url(r'^%s/benefits/?$' % PREFIX, BenefitPlanCreationView.as_view(), name='benefit_post_api'),
    url(r'^%s/templates/?$' % PREFIX, templates),
    url(r'^%s/documents/?$' % PREFIX, documents),

    # Company features api
    url(r'^%s/company_features/(?P<pk>\w+)/?$' % PREFIX, CompanyFeaturesView.as_view(), name='company_features_api'),
    url(r'^%s/all_company_features/(?P<company_id>\w+)/?$' % PREFIX, CompleteCompanyApplicationFeaturesView.as_view(), name='all_company_features_api'),
    url(r'^%s/all_company_user_features/(?P<company_id>\w+)/(?P<user_id>\w+)/?$' % PREFIX, CompleteCompanyUserApplicationFeaturesView.as_view(), name='company_user_all_features_api'),

    # Company groups api
    url(r'^%s/company/(?P<company_id>\w+)/groups/?$' % PREFIX, CompanyGroupView.as_view(), name='company_group_by_company_api'),

    url(r'^%s/company_group/(?P<pk>\w+)/?$' % PREFIX, CompanyGroupView.as_view(), name='company_group_api'),

    url(r'^%s/company_group/(?P<pk>\w+)/members/?$' % PREFIX, CompanyGroupMemberCompanyGroupView.as_view(), name='company_group_company_group_member_api'),

    url(r'^%s/company_group_member/(?P<pk>\w+)/?$' % PREFIX, CompanyGroupMemberView.as_view(), name='company_group_member_api'),

    url(r'^%s/company/(?P<pk>\w+)/group_member/?$' % PREFIX, CompanyGroupMemberCompanyView.as_view(), name='company_group_member_company_api'),

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

    url(r'^%s/company_group/(?P<company_group_id>\w+)/company_fsa/?$' % PREFIX,
        CompanyGroupFsaPlanByCompanyGroupView.as_view(),
        name='company_group_fsa_plan_api'),

    url(r'^%s/company_fsa/(?P<pk>\w+)/company_group_plans/?$' % PREFIX,
        CompanyGroupFsaPlanByCompanyPlanView.as_view(),
        name='company_group_fsa_plan_by_company_plan_api'),

    # Life insurance api
    url(r'^%s/brokers/(?P<pk>\w+)/life_insurance_plan/?$' % PREFIX,
        LifeInsurancePlanView.as_view(), name='broker_life_insurance_api'),

    url(r'^%s/users/(?P<pk>\w+)/life_insurance/?$' % PREFIX,
        UserCompanyLifeInsuranceView.as_view(), name='user_life_insurance_api'),

    url(r'^%s/company_users/(?P<pk>\w+)/life_insurance/?$' % PREFIX,
        CompanyUsersLifeInsuranceView.as_view(), name='company_users_life_insurance_api'),

    url(r'^%s/company/(?P<pk>\w+)/life_insurance_plan/?$' % PREFIX,
        CompanyLifeInsurancePlanView.as_view(), name='company_life_insurance_plan_api'),

    url(r'^%s/company_group/(?P<company_group_id>\w+)/basic_life_insurance_plan/?$' % PREFIX,
        CompanyGroupBasicLifeInsurancePlanByCompanyGroupView.as_view(),
        name='company_group_basic_life_insurance_plan_api'),

    url(r'^%s/user/(?P<user_id>\w+)/life_insurance_plan/(?P<pk>\w+)/premium/?$' % PREFIX,
        CompanyLifeInsuranceEmployeePremiumView.as_view(), name='user_company_life_insurance_premium_api'),

    url(r'^%s/company_basic_life_insurance_plan/(?P<pk>\w+)/company_group_plans/?$' % PREFIX,
        CompanyGroupBasicLifeInsurancePlanByCompanyPlanView.as_view(),
        name='company_group_basic_life_insurance_plan_by_company_plan_api'),

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

    url(r'^%s/company_group/(?P<company_group_id>\w+)/company_suppl_life/?$' % PREFIX,
        CompanyGroupSupplementalLifeInsurancePlanByCompanyGroupView.as_view(),
        name='company_group_supplemental_life_insurance_plan_api'),

    url(r'^%s/company_suppl_life/(?P<pk>\w+)/company_group_plans/?$' % PREFIX,
        CompanyGroupSupplementalLifeInsurancePlanByCompanyPlanView.as_view(),
        name='company_group_supplemental_life_insurance_plan_by_company_plan_api'),


    # STD insurance api
    url(r'^%s/brokers/(?P<pk>\w+)/std_insurance_plan/?$' % PREFIX,
        StdInsurancePlanView.as_view(), name='broker_std_insurance_api'),

    url(r'^%s/users/(?P<pk>\w+)/std_insurance/?$' % PREFIX,
        UserCompanyStdInsuranceView.as_view(), name='user_std_insurance_api'),

    url(r'^%s/company_users/(?P<pk>\w+)/std_insurance/?$' % PREFIX,
        CompanyUsersStdInsuranceView.as_view(), name='company_users_std_insurance_api'),

    url(r'^%s/company/(?P<pk>\w+)/std_insurance_plan/?$' % PREFIX,
        CompanyStdInsurancePlanView.as_view(), name='company_std_insurance_plan_api'),

    url(r'^%s/user/(?P<user_id>\w+)/std_insurance/(?P<pk>\w+)/premium/?$' % PREFIX,
        CompanyStdInsuranceEmployeePremiumView.as_view(), name='user_company_std_insurance_premium_api'),

    url(r'^%s/company_group/(?P<company_group_id>\w+)/std_insurance/?$' % PREFIX,
        CompanyGroupStdInsurancePlanByCompanyGroupView.as_view(),
        name='company_group_std_insurance_plan_api'),

    url(r'^%s/std_insurance/(?P<pk>\w+)/company_group_plans/?$' % PREFIX,
        CompanyGroupStdInsurancePlanByCompanyPlanView.as_view(),
        name='company_group_std_insurance_plan_by_company_plan_api'),



    # LTD insurance api
    url(r'^%s/brokers/(?P<pk>\w+)/ltd_insurance_plan/?$' % PREFIX,
        LtdInsurancePlanView.as_view(), name='broker_ltd_insurance_api'),

    url(r'^%s/users/(?P<pk>\w+)/ltd_insurance/?$' % PREFIX,
        UserCompanyLtdInsuranceView.as_view(), name='user_ltd_insurance_api'),

    url(r'^%s/company_users/(?P<pk>\w+)/ltd_insurance/?$' % PREFIX,
        CompanyUsersLtdInsuranceView.as_view(), name='company_users_ltd_insurance_api'),

    url(r'^%s/company/(?P<pk>\w+)/ltd_insurance_plan/?$' % PREFIX,
        CompanyLtdInsurancePlanView.as_view(), name='company_ltd_insurance_plan_api'),

    url(r'^%s/user/(?P<user_id>\w+)/ltd_insurance/(?P<pk>\w+)/premium/?$' % PREFIX,
        CompanyLtdInsuranceEmployeePremiumView.as_view(), name='user_company_ltd_insurance_premium_api'),

    url(r'^%s/company_group/(?P<company_group_id>\w+)/ltd_insurance/?$' % PREFIX,
        CompanyGroupLtdInsurancePlanByCompanyGroupView.as_view(),
        name='company_group_ltd_insurance_plan_api'),

    url(r'^%s/ltd_insurance/(?P<pk>\w+)/company_group_plans/?$' % PREFIX,
        CompanyGroupLtdInsurancePlanByCompanyPlanView.as_view(),
        name='company_group_ltd_insurance_plan_by_company_plan_api'),

    # HRA api
    url(r'^%s/hra_plan/(?P<pk>\w+)/?$' % PREFIX,
        HraPlanView.as_view(), name='hra_plan_api'),

    url(r'^%s/company_hra_plan/(?P<pk>\w+)/?$' % PREFIX,
        CompanyHraPlanView.as_view(), name='company_hra_plan_api'),

    url(r'^%s/company/(?P<company_id>\w+)/company_hra_plan/?$' % PREFIX,
        CompanyHraPlanByCompanyView.as_view(), name='company_hra_plan_by_company_api'),

    url(r'^%s/person_company_hra_plan/(?P<pk>\w+)/?$' % PREFIX,
        PersonCompanyHraPlanView.as_view(), name='person_company_hra_plan_api'),

    url(r'^%s/person/(?P<person_id>\w+)/person_company_hra_plan/?$' % PREFIX,
        PersonCompanyHraPlanByPersonView.as_view(), name='person_company_hra_plan_by_person_api'),

    url(r'^%s/company_group/(?P<company_group_id>\w+)/company_hra/?$' % PREFIX,
        CompanyGroupHraPlanByCompanyGroupView.as_view(),
        name='company_group_hra_plan_api'),

    url(r'^%s/company_hra/(?P<pk>\w+)/company_group_plans/?$' % PREFIX,
        CompanyGroupHraPlanByCompanyPlanView.as_view(),
        name='company_group_hra_plan_by_company_plan_api'),

    # Commuter api
    url(r'^%s/company_commuter_plan/(?P<pk>\w+)/?$' % PREFIX,
        CompanyCommuterPlanView.as_view(), name='company_commuter_plan_api'),

    url(r'^%s/company/(?P<company_id>\w+)/company_commuter_plan/?$' % PREFIX,
        CompanyCommuterPlanByCompanyView.as_view(), name='company_commuter_plan_by_company_api'),

    url(r'^%s/person_company_commuter_plan/(?P<pk>\w+)/?$' % PREFIX,
        PersonCompanyCommuterPlanView.as_view(), name='person_company_commuter_plan_api'),

    url(r'^%s/person/(?P<person_id>\w+)/person_company_commuter_plan/?$' % PREFIX,
        PersonCompanyCommuterPlanByPersonView.as_view(), name='person_company_commuter_plan_by_person_api'),

    url(r'^%s/company_group/(?P<company_group_id>\w+)/company_commuter/?$' % PREFIX,
        CompanyGroupCommuterPlanByCompanyGroupView.as_view(),
        name='company_group_commuter_plan_api'),

    url(r'^%s/company_commuter/(?P<pk>\w+)/company_group_plans/?$' % PREFIX,
        CompanyGroupCommuterPlanByCompanyPlanView.as_view(),
        name='company_group_commuter_plan_by_company_plan_api'),

    # Extra Benefits api
    url(r'^%s/company_extra_benefit_plan/(?P<pk>\w+)/?$' % PREFIX,
        CompanyExtraBenefitPlanView.as_view(), name='company_extra_benefit_plan_api'),

    url(r'^%s/company/(?P<company_id>\w+)/company_extra_benefit_plan/?$' % PREFIX,
        CompanyExtraBenefitPlanByCompanyView.as_view(), name='company_extra_benefit_plan_by_company_api'),

    url(r'^%s/person_company_extra_benefit_plan/(?P<pk>\w+)/?$' % PREFIX,
        PersonCompanyExtraBenefitPlanView.as_view(), name='person_company_extra_benefit_plan_api'),

    url(r'^%s/person/(?P<person_id>\w+)/person_company_extra_benefit_plan/?$' % PREFIX,
        PersonCompanyExtraBenefitPlanByPersonView.as_view(), name='person_company_extra_benefit_plan_by_person_api'),

    # HSA Benefits api
    url(r'^%s/company/hsa/(?P<pk>\w+)/?$' % PREFIX,
        CompanyHsaPlanView.as_view(), name='company_hsa_plan_api'),

    url(r'^%s/person/(?P<person_id>\w+)/hsa/?$' % PREFIX,
        PersonCompanyGroupHsaPlanByPersonView.as_view(), name='person_hsa_plan_by_person_api'),

    url(r'^%s/person_hsa/(?P<pk>\w+)/hsa/?$' % PREFIX,
        PersonCompanyGroupHsaPlanView.as_view(), name='person_hsa_plan_api'),

    url(r'^%s/company/(?P<company_id>\w+)/hsa/?$' % PREFIX,
        CompanyHsaPlanByCompanyView.as_view(), name='company_hsa_plan_company_api'),

    url(r'^%s/company_group/(?P<company_group_id>\w+)/hsa/?$' % PREFIX,
        CompanyGroupHsaPlanByCompanyGroupView.as_view(),
        name='company_group_hsa_plan_group_api'),

    url(r'^%s/company_hsa_plan/(?P<pk>\w+)/company_group_plans/?$' % PREFIX,
        CompanyGroupHsaPlanByCompanyPlanView.as_view(),
        name='company_group_hsa_plan_company_plan_api'),

    # util api
    url(r'^%s/onboard_email/?$' % PREFIX, send_onboard_email),

    # UserData Change Email api
    url(r'^%s/user_data_email/?$' % PREFIX, UserDataChangeEmailView.as_view()),

    # Reporting API
    url(r'^%s/person/(?P<person_id>\w+)/benefits/?$' % PREFIX,
        PersonEnrollmentSummaryView.as_view(), name='person_benefit_summary_api'),

    url(r'^%s/company/(?P<company_id>\w+)/benefits/?$' % PREFIX,
        CompanyBenefitAvailabilityView.as_view(), name='company_benefit_availability_api'),

    url(r'^%s/company/(?P<comp_id>\w+)/enrollment_summary/?$' % PREFIX,
        CompanyEnrollmentSummaryView.as_view(), name='company_enrollment_summary_api'),

    # upload API
    url(r'^%s/users/(?P<pk>\w+)/uploads/?$' % PREFIX, UserUploadView.as_view(), name='uploads_by_user'),

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
    url(r'^%s/users/(?P<user_id>\w+)/uploads_for/?$' % PREFIX,
        UploadForUserView.as_view(),
        name='upload_for_user_api'),

    url(r'^%s/employee_profile/(?P<pk>\w+)/?$' % PREFIX,
        EmployeeProfileView.as_view(),
        name='employee_profile_api'),
    url(r'^%s/person/(?P<person_id>\w+)/company/(?P<company_id>\w+)/employee_profile/?$' % PREFIX,
        EmployeeProfileByPersonCompanyView.as_view(),
        name='employee_profile_by_person_company_api'),
    url(r'^%s/company/(?P<company_id>\w+)/user/(?P<user_id>\w+)/employee_profile/?$' % PREFIX,
        EmployeeProfileByCompanyUserView.as_view(),
        name='employee_profile_by_company_user_api'),
    url(r'^%s/company/(?P<company_id>\w+)/employee_profiles/?$' % PREFIX,
        EmployeeProfilesByCompanyView.as_view(),
        name='employee_profiles_by_company_api'),
    url(r'^%s/company/(?P<company_id>\w+)/pin/(?P<pin>\w+)/employee_profile/?$' % PREFIX,
        EmployeeProfileByCompanyPinView.as_view(),
        name='employee_profile_by_company_pin_api'),

    url(r'^%s/employee_compensation/(?P<pk>\w+)/?$' % PREFIX,
        EmployeeCompensationView.as_view(),
        name='employee_compensation_api'),
    url(r'^%s/person/(?P<person_id>\w+)/employee_compensation/?$' % PREFIX,
        EmployeeCompensationByPersonView.as_view(),
        name='employee_compensation_by_person_api'),

    url(r'^%s/employee_timetracking/(?P<pk>\w+)/?$' % PREFIX,
        EmployeeTimeTrackingView.as_view(),
        name='employee_timetracking_api'),
    url(r'^%s/person/(?P<person_id>\w+)/employee_timetracking/?$' % PREFIX,
        EmployeeTimeTrackingByPersonCompanyView.as_view(),
        name='employee_timetracking_by_person_api'),

    url(r'^%s/benefit_update_reasons/?$' % PREFIX, SysBenefitUpdateReasonView.as_view(), name='sys_benefit_update_reason_api'),

    url(r'^%s/companies/(?P<pk>\w+)/1095_c/?$' % PREFIX,
        Company1095CView.as_view(),
        name='company_1095_c_api'),
    url(r'^%s/company/(?P<company_id>\w+)/person/(?P<person_id>\w+)/1095_c/?$' % PREFIX,
        Employee1095CView.as_view(),
        name='employee_1095_c_api'),
    url(r'^%s/companies/(?P<pk>\w+)/1094_c/?$' % PREFIX,
        Company1094CView.as_view(),
        name='company_1094_c_api'),

    url(r'^%s/company/(?P<company_id>\w+)/batch_account_creation/parse_account_data/?$' % PREFIX,
        AccountInfoListParseView.as_view(),
        name='batch_account_creation_parse_data_api'),

    url(r'^%s/company/(?P<company_id>\w+)/batch_account_creation/batch_create/?$' % PREFIX,
        BatchAccountCreationView.as_view(),
        name='batch_account_creation_batch_create_api'),

    url(r'^%s/company/(?P<company_id>\w+)/batch_employee_organization_import/parse_organization_data/?$' % PREFIX,
        BatchEmployeeOrganizationImportRawDataParseView.as_view(),
        name='batch_employee_organization_import_parse_data_api'),

    url(r'^%s/company/(?P<company_id>\w+)/batch_employee_organization_import/batch_import/?$' % PREFIX,
        BatchEmployeeOrganizationImportView.as_view(),
        name='batch_employee_organization_import_api'),

    url(r'^%s/company/(?P<company_id>\w+)/employee_management/termination/?$' % PREFIX,
        EmployeeTerminationView.as_view(),
        name='employee_management_termination_api'),

    url(r'^%s/1095_c_periods/?$' % PREFIX, ACA1095CPeriodsView.as_view(), name='ACA_1095_c_periods_api'),

    url(r'^%s/1094_c_certificiations/?$' % PREFIX, ACA1094CEligibilityCertificationView.as_view(), name='ACA_1094_c_cert_api'),

    # Onboarding
    url(r'^%s/onboarding_step_states/(?P<pk>\w+)/?$' % PREFIX,
        UserOnboardingStepStateView.as_view(), name='user_onboarding_step_states_api'),
    url(r'^%s/onboarding_step_states/?$' % PREFIX,
        UserOnboardingStepStateView.as_view(), name='user_onboarding_step_states_post_api'),
    url(r'^%s/users/(?P<pk>\w+)/onboarding_step_states/?$' % PREFIX,
        UserOnboardingStepStateByUserView.as_view(), name='user_onboarding_step_states_by_user_api'),

    # Company service provider_type
    url(r'^%s/company_service_provider/(?P<pk>\w+)/?$' % PREFIX,
        CompanyServiceProviderView.as_view(), name='company_service_provider_api'),
    url(r'^%s/company_service_provider/?$' % PREFIX,
        CompanyServiceProviderView.as_view(), name='company_service_provider_post_api'),
    url(r'^%s/company/(?P<company_id>\w+)/company_service_providers/?$' % PREFIX,
        CompanyServiceProviderByCompanyView.as_view(), name='company_service_provider_by_company_api'),

    # Workers' Comp
    url(r'^%s/phraseologys/?$' % PREFIX,
        AllPhraseologyView.as_view(), name='all_phraseology_api'),
    url(r'^%s/company_phraseologys/(?P<pk>\w+)/?$' % PREFIX,
        CompanyPhraseologyView.as_view(), name='company_phraseology_api'),
    url(r'^%s/company_phraseologys/?$' % PREFIX,
        CompanyPhraseologyView.as_view(), name='company_phraseology_post_api'),
    url(r'^%s/company/(?P<company_id>\w+)/phraseologys/?$' % PREFIX,
        CompanyPhraseologyByCompanyView.as_view(), name='company_phraseology_by_company_api'),
    url(r'^%s/employee_phraseologys/(?P<pk>\w+)/?$' % PREFIX,
        EmployeePhraseologyView.as_view(), name='employee_phraseology_api'),
    url(r'^%s/employee_phraseologys/?$' % PREFIX,
        EmployeePhraseologyView.as_view(), name='employee_phraseology_post_api'),
    url(r'^%s/person/(?P<person_id>\w+)/phraseologys/?$' % PREFIX,
        EmployeePhraseologyByEmployeePersonView.as_view(), name='employee_phraseology_by_person_api'),

    # Company Metadata
    url(r'^%s/company_departments/(?P<pk>\w+)/?$' % PREFIX,
        CompanyDepartmentView.as_view(), name='company_department_api'),
    url(r'^%s/company_departments/?$' % PREFIX,
        CompanyDepartmentView.as_view(), name='company_department_post_api'),
    url(r'^%s/company/(?P<company_id>\w+)/departments/?$' % PREFIX,
        CompanyDepartmentByCompanyView.as_view(), name='company_department_by_company_api'),

    url(r'^%s/company_jobs/(?P<pk>\w+)/?$' % PREFIX,
        CompanyJobView.as_view(), name='company_job_api'),
    url(r'^%s/company_jobs/?$' % PREFIX,
        CompanyJobView.as_view(), name='company_job_post_api'),
    url(r'^%s/company/(?P<company_id>\w+)/jobs/?$' % PREFIX,
        CompanyJobByCompanyView.as_view(), name='company_job_by_company_api'),

    url(r'^%s/company_divisions/(?P<pk>\w+)/?$' % PREFIX,
        CompanyDivisionView.as_view(), name='company_division_api'),
    url(r'^%s/company_divisions/?$' % PREFIX,
        CompanyDivisionView.as_view(), name='company_division_post_api'),
    url(r'^%s/company/(?P<company_id>\w+)/divisions/?$' % PREFIX,
        CompanyDivisionByCompanyView.as_view(), name='company_division_by_company_api'),    

    # Integration

    # # Common
    url(r'^%s/companies/(?P<company_id>\w+)/integration_providers?$' % PREFIX, CompanyIntegrationProvidersByCompanyView.as_view(), name='company_integration_providers_api'),

    # # Advantage Payroll
    url(r'^%s/companies/(?P<company_id>\w+)/advantage_payroll/setup_csv?$' % PREFIX, AdvantagePayrollClientSetupCsvView.as_view(), name='company_advantage_payroll_setup_csv_api'),
    url(r'^%s/companies/(?P<company_id>\w+)/advantage_payroll/period_export_csv/from/(?P<from_year>\d+)/(?P<from_month>\d+)/(?P<from_day>\d+)/to/(?P<to_year>\d+)/(?P<to_month>\d+)/(?P<to_day>\d+)/?$' % PREFIX, AdvantagePayrollPeriodExportCsvView.as_view(), name='company_advantage_payroll_period_export_csv_api'),

    # # Connect Payroll
    url(r'^%s/companies/(?P<company_id>\w+)/connect_payroll/period_export_csv/from/(?P<from_year>\d+)/(?P<from_month>\d+)/(?P<from_day>\d+)/to/(?P<to_year>\d+)/(?P<to_month>\d+)/(?P<to_day>\d+)/?$' % PREFIX, ConnectPayrollPeriodExportCsvView.as_view(), name='company_connect_payroll_period_export_csv_api'),
    url(r'^%s/companies/(?P<company_id>\w+)/connect_payroll/employee_frontpage_csv?$' % PREFIX, ConnectPayrollEmployeeFrontPageCsvView.as_view(), name='company_connect_payroll_employee_frontpage_csv_api'),
    
    # Logging
    url(r'^%s/log/level/(?P<level>\w+)/?$' % PREFIX, LoggingServiceView.as_view(), name="logging_api"),

    # Admin APIs

    ## API to generate a list of passwords with proper randomization
    url(r'^%s/password_generator/(?P<num_passwords>\d+)/?$' % ADMIN_PREFIX, PasswordGeneratorView.as_view(), name="password_generator_api"),
    
    ## API to correct SSN format for all persons on record. This only affect SSNs that are not in valid format. i.e. 9-digits
    url(r'^%s/ssn_format_correction/?$' % ADMIN_PREFIX, SsnFormatCorrectionForAllView.as_view(), name="ssn_format_correction_for_all_api")
)

urlpatterns = format_suffix_patterns(urlpatterns)
