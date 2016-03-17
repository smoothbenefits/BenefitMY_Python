var BenefitMyApp = angular.module('BenefitMyApp',[
    'ngResource',
    'ui.router',
    'ui.mask',
    'ui.utils.masks',
    'ui.bootstrap',
    'angularFileUpload',
    'angularSpinner',
    'isteven-multi-select',
    'blockUI',
    'environment',
    'benefitmyDomainModelFactories',
    'benefitmyTimeTrackingModelFactories',
    'benefitmyService',
    'benefitmyApp.constants',
    'benefitmyApp.users.controllers',
    'benefitmyApp.brokers.controllers',
    'benefitmyApp.employers.controllers',
    'benefitmyApp.employees.controllers']);

//Setup underscore:

var underscore = angular.module('underscore', []);
underscore.factory('_', function(){
    return window._;
});

String.prototype.capitalize = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
};

var DATE_FORMAT_STRING = 'dddd, MMM Do, YYYY';
var SHORT_DATE_FORMAT_STRING = 'MM/DD/YYYY';
var STORAGE_DATE_FORMAT_STRING = 'YYYY-MM-DD';
var DATE_TIME_FORMAT_STRING = 'LLLL';

// The URL to which logging to server side should be posted to
var LOGGING_SERVER_URL = '/api/v1/log/level/error'

BenefitMyApp.config(['$resourceProvider', '$httpProvider', function($resourceProvider, $httpProvider) {
  // Don't strip trailing slashes from calculated URLs
  $resourceProvider.defaults.stripTrailingSlashes = false;

  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

// Config the spinner style
BenefitMyApp.config(['usSpinnerConfigProvider', function (usSpinnerConfigProvider) {
    usSpinnerConfigProvider.setDefaults({
        scale: '3'
    });
}]);

// Config the block ui component
BenefitMyApp.config(function(blockUIConfig) {

  blockUIConfig.template = '<div class="block-ui-overlay"><span us-spinner></span></div>';

  // Change the default delay before the blocking is visible
  // Setup some delay would increase the pages' responsiveness
  blockUIConfig.delay = 250;
});

// Configure global error logging
// - Preserves the default local logging to console
// - Add logging to server
BenefitMyApp.config(function ($provide) {
  $provide.decorator("$exceptionHandler",
    ['$delegate', '$window', '$log', '$injector', 'BrowserDetectionService',
    function($delegate, $window, $log, $injector, BrowserDetectionService) {
    return function (exception, cause) {
        // now try to log the error to the server side.
        try {
            // use our traceService to generate a stack trace
            var stackTrace = printStackTrace({e: exception});
            var errorMessage = exception.toString();

            var $http = $injector.get("$http");

            var request = {
              method: 'POST',
              url: LOGGING_SERVER_URL,
              headers: {
                'Content-Type': 'application/json'
              },
              data: angular.toJson({
                  url: $window.location.href,
                  message: errorMessage,
                  browser: BrowserDetectionService.getCurrentBrowser(),
                  type: "exception",
                  stackTrace: stackTrace.join('\n\n')
                })
            };

            // Use $http to get CSRF token
            $http(request).then(function(){}, function(error) {
              $log.warn("Error server-side logging failed");
              $log.log(error);
            });
        } catch (loggingError) {
            $log.warn("Error server-side logging failed");
            $log.log(loggingError);
        }

        // Delegate to the default behavior
        $delegate(exception, cause);
    }
  }])
});

BenefitMyApp.config(['envServiceProvider', function(envServiceProvider) {
    envServiceProvider.config({
        domains: {
            localhost: ['localhost'],
            stage:['staging.workbenefits.me', 'staging.workbenefitsme.com', 'staging.benefitmy.com'],
            demo: ['demo.workbenefits.me', 'demo.workbenefitsme.com', 'demo.benefitmy.com'],
            production: ['app.workbenefits.me', 'app.workbenefitsme.com', 'app.benefitmy.com']
        },
        vars: {
            localhost: {
                timeTrackingUrl: 'http://localhost:6999/'
            },
            stage: {
                timeTrackingUrl: 'http://stage.timetracking.workbenefits.me/'
            },
            demo: {
                timeTrackingUrl: 'http://stage.timetracking.workbenefits.me/'
            },
            production: {
                timeTrackingUrl: 'https://timetracking.workbenefits.me/'
            }
        }
    });

    // run the environment check, so the comprobation is made
    // before controllers and services are built
    envServiceProvider.check();
}]);

BenefitMyApp.config(['$stateProvider', '$urlRouterProvider',
    function ($stateProvider, $urlRouterProvider) {
        // For any unmatched url, redirect to state "/"
        $urlRouterProvider.otherwise("/");

        $stateProvider.
            state('settings', {
                url: "/user/:user_id/settings?onboard",
                templateUrl: '/static/partials/settings.html',
                controller: 'settingsController'
            }).
            state('/broker', {
                url: "/broker",
                templateUrl: '/static/partials/clients.html',
                controller: 'clientsController'
            }).
            state('/broker/add_client', {
                url: '/broker/add_client',
                templateUrl: '/static/partials/add_client.html'
            }).
            state('/broker/benefits/:clientId', {
                url: '/broker/benefits/:clientId',
                templateUrl: '/static/partials/view_benefits.html',
                controller: 'benefitsController'
            }).
            state('/broker/employee_list', {
              url: '/broker/client/:client_id/employees',
              templateUrl: '/static/partials/broker_edit_employee_info.html',
              controller: 'brokerEmployeeEdit'
            }).
            state('broker_add_benefit', {
                url: '/broker/add_benefit/:clientId',
                templateUrl: '/static/partials/benefit_addition/main.html',
                controller: 'brokerAddBenefits'
            }).
            state('broker_add_benefit.health', {
                url: '/health',
                templateUrl: '/static/partials/benefit_addition/tab_health_benefit.html',
                controller: 'brokerAddHealthBenefits'
            }).
            state('broker_add_benefit.basic_life_insurance', {
                url: '/basic_life',
                templateUrl: '/static/partials/benefit_addition/tab_basic_life.html',
                controller: 'brokerAddBasicLifeInsurance'
            }).
            state('broker_add_benefit.supplemental_life_insurance', {
                url: '/supplemental_life',
                templateUrl: '/static/partials/benefit_addition/tab_supplemental_life.html',
                controller: 'brokerAddSupplementalLifeInsurance'
            }).
            state('broker_add_benefit.std', {
                url: '/std',
                templateUrl: '/static/partials/benefit_addition/tab_std.html',
                controller: 'brokerAddStdPlanController'
            }).
            state('broker_add_benefit.ltd', {
                url: '/ltd',
                templateUrl: '/static/partials/benefit_addition/tab_ltd.html',
                controller: 'brokerAddLtdPlanController'
            }).
            state('broker_add_benefit.fsa', {
                url: '/fsa',
                templateUrl: '/static/partials/benefit_addition/tab_fsa.html',
                controller: 'brokerAddFsaPlanController'
            }).
            state('broker_add_benefit.hsa', {
                url: '/hsa',
                templateUrl: '/static/partials/benefit_addition/tab_hsa.html',
                controller: 'brokerAddHsaPlanController'
            }).
            state('broker_add_benefit.hra', {
                url: '/hra',
                templateUrl: '/static/partials/benefit_addition/tab_hra.html',
                controller: 'brokerAddHraPlanController'
            }).
            state('broker_add_benefit.commuter', {
                url: '/commuter',
                templateUrl: '/static/partials/benefit_addition/tab_commuter.html',
                controller: 'brokerAddCommuterPlanController'
            }).
            state('broker_add_benefit.extra_benefit', {
                url: '/extra_benefit',
                templateUrl: '/static/partials/benefit_addition/tab_extra_benefit.html',
                controller: 'brokerAddExtraBenefitPlanController'
            }).
            state('broker_benefit_selected', {
                url: '/broker/benefit/selected/:client_id',
                templateUrl: '/static/partials/selected_benefits_company.html',
                controller: 'selectedBenefitsController'
            }).
            state('broker_view_employee_family', {
              url: '/broker/view_family/:employeeId',
              templateUrl: '/static/partials/family_management/base.html',
              controller: 'brokerEmployeeFamilyController'
            }).
            state('broker_company_employee_personal_info', {
                url: '/broker/employee/:employee_id/information',
                templateUrl: '/static/partials/employee_profile/edit_personal_info.html',
                controller: 'brokerEmployeeInfoController'
            }).
            state('broker_company_group', {
              url: '/broker/company/:company_id/groups',
              templateUrl: '/static/partials/client_management/company_group.html',
              controller: 'CompanyBenefitGroupManagementController'
            }).
            state('broker_company_aca_report', {
                url: '/broker/company/:company_id/aca_report',
                templateUrl: '/static/partials/aca/aca_report_card.html',
                controller: 'companyAcaReport'
            }).
            state('/broker/benefit/add_details/:client_id/:benefit_id', {
                url: '/broker/benefit/add_details/:client_id/:benefit_id',
                templateUrl:'/static/partials/benefit_detail_input.html',
                controller: 'benefitInputDetailsController'
            }).
            state('/broker/employee/:employee_id', {
                url: '/broker/employee/:employee_id?cid',
                templateUrl: '/static/partials/employee_detail.html',
                controller: 'brokerEmployeeController'
            }).
            state('broker_company_employee_enrollment',{
                url:'/broker/client/:company_id/employee/:employee_id/enrollment',
                templateUrl: '/static/partials/company_employee_selection.html',
                controller: 'brokerEmployeeEnrollmentController'
            }).
            state('/', {
                url: '/',
                template: '',
                controller:'findViewController'
            }).
            state('/admin',{
                url: '/admin',
                templateUrl: '/static/partials/employer_dashboard.html',
                controller: 'employerHome'
            }).
            state('aca_report', {
              url: '/admin/reports/aca/:company_id',
              templateUrl: '/static/partials/aca/aca_report_card.html',
              controller: 'employerAcaReport'
            }).
            state('/admin/broker/add/:company_id', {
                url: '/admin/broker/add/:company_id',
                templateUrl:'/static/partials/add_broker.html',
                controller:'employerUser'
            }).
            state('/admin/broker/:company_id', {
                url: '/admin/broker/:company_id',
                templateUrl:'/static/partials/view_broker.html',
                controller:'employerUser'
            }).
            state('/admin/benefits/:company_id', {
                url: '/admin/benefits/:company_id',
                templateUrl:'/static/partials/view_benefits.html',
                controller:'employerBenefits'
            }).
            state('/admin/employee/add/:company_id', {
                url: '/admin/employee/add/:company_id',
                templateUrl:'/static/partials/add_employee.html',
                controller:'employerUser'
            }).
            state('batch_add_employees', {
                url: '/admin/employee/batch_add/:company_id',
                templateUrl:'/static/partials/batch_employee_addition/main.html',
                abstract: true,
                controller:'batchEmployeeAdditionController'
            }).
            state('batch_add_employees.input', {
                url: '',
                templateUrl: '/static/partials/batch_employee_addition/partial_input.html',
                controller:'batchEmployeeAdditionController'
            }).
            state('batch_add_employees.parse_result', {
                url: '/parse_result',
                templateUrl: '/static/partials/batch_employee_addition/partial_parse_result.html',
                controller:'batchEmployeeAdditionController'
            }).
            state('batch_add_employees.save_result', {
                url: '/save_result',
                templateUrl: '/static/partials/batch_employee_addition/partial_save_result.html',
                controller:'batchEmployeeAdditionController'
            }).
            state('batch_employee_organization_import', {
                url: '/admin/employee/batch_organization_import/:company_id',
                templateUrl:'/static/partials/batch_employee_organization/main.html',
                abstract: true,
                controller:'batchEmployeeOrganizationImportController'
            }).
            state('batch_employee_organization_import.input', {
                url: '',
                templateUrl: '/static/partials/batch_employee_organization/partial_input.html',
                controller:'batchEmployeeOrganizationImportController'
            }).
            state('batch_employee_organization_import.parse_result', {
                url: '/parse_result',
                templateUrl: '/static/partials/batch_employee_organization/partial_parse_result.html',
                controller:'batchEmployeeOrganizationImportController'
            }).
            state('batch_employee_organization_import.save_result', {
                url: '/save_result',
                templateUrl: '/static/partials/batch_employee_organization/partial_save_result.html',
                controller:'batchEmployeeOrganizationImportController'
            }).
            state('document_templates', {
                url: '/admin/documents/template/:company_id',
                templateUrl:'/static/partials/documents/view_templates.html',
                controller:'employerLetterTemplate'
            }).
            state('document_templates_edit', {
                url: '/admin/documents/template/:company_id/edit/:template_id',
                templateUrl:'/static/partials/documents/modify_template.html',
                controller:'employerModifyTemplate'
            }).
            state('/admin/employee/:company_id', {
                url: '/admin/employee/:company_id',
                templateUrl:'/static/partials/view_employee.html',
                controller:'employerUser'
            }).
            state('/admin/documents/create/:company_id/:employee_id', {
                url: '/admin/documents/create/:company_id/:employee_id?type',
                templateUrl:'/static/partials/documents/create.html',
                controller:'employerCreateDocument'
            }).
            state('employer_batch_create_documents', {
                url: '/admin/documents/batch_create/:company_id/:template_id',
                templateUrl:'/static/partials/documents/batch_create_documents.html',
                controller:'employerBatchCreateDocuments'
            }).
            state('/admin/documents/view/:company_id/:employee_id', {
                url: '/admin/documents/view/:company_id/:employee_id?type',
                templateUrl:'/static/partials/documents/view.html',
                controller:'employerViewDocument'
            }).
            state('/admin/view_draft/:company_id/:employee_id/:document_type_id', {
                url: '/admin/view_draft/:company_id/:employee_id/:document_type_id',
                templateUrl: '/static/partials/view_draft.html',
                controller: 'employerViewDraft'
            }).
            state('/admin/employee_detail/:company_id', {
                url: '/admin/employee_detail/:company_id?eid',
                templateUrl: '/static/partials/employee_detail.html',
                controller: 'employerViewEmployeeDetail'
            }).
            state('admin_benefit_elections',{
                url: '/admin/benefit/election/:company_id',
                templateUrl:'/static/partials/selected_benefits_company.html',
                controller: 'employerBenefitsSelected'
            }).
            state('admin_employee_benefit_selection', {
                url: '/admin/benefit/:company_id/selection/:employee_id',
                templateUrl: '/static/partials/company_employee_selection.html',
                controller:'employerEmployeeSelected'
            }).
            state('admin_employee_uploads',{
                url: '/admin/:company_id/employee/:employee_id/uploads',
                templateUrl: '/static/partials/view_employee_uploads.html',
                controller: 'employerViewUploads'
            }).
            state('admin_time_off', {
              url: '/admin/timeoff',
              templateUrl: '/static/partials/timeoff/timeoff_base.html',
              controller: 'employerTimeOffController'
            }).
            state('admin_timesheet',{
                url: '/admin/:company_id/timesheet',
                templateUrl: '/static/partials/work_timesheet/timesheet_base.html',
                controller: 'employerViewTimesheet'
            }).
            state('admin_timepunchcards', {
                url: '/admin/:company_id/time_punch_cards',
                templateUrl: '/static/partials/time_punch_card/time_punch_card_base.html',
                controller: 'employerViewTimePunchCards'
            }).
            state('admin_service_provider', {
              url: '/admin/service_provider',
              templateUrl: '/static/partials/company_service_provider/company_service_provider_base.html',
              controller: 'EmployerCompanyServiceProvider'
            }).
            state('/employee',{
                url: '/employee',
                templateUrl: '/static/partials/employee_dashboard.html',
                controller: 'employeeHome'
            }).
            state('employee_benefit_signup', {
                url: '/employee/benefits/:employee_id',
                templateUrl: '/static/partials/benefit_selection/main.html',
                controller:'employeeBenefitsSignup',
                params: { updateReason: null }
            }).
            state('employee_benefit_signup.health', {
                url: '/health_benefits',
                templateUrl: '/static/partials/benefit_selection/tab_health_benefits.html',
                controller:'healthBenefitsSignup'
            }).
            state('employee_benefit_signup.fsa', {
                url: '/fsa',
                templateUrl: '/static/partials/benefit_selection/tab_fsa.html',
                controller:'fsaBenefitsSignup'
            }).
            state('employee_benefit_signup.hsa', {
                url: '/hsa',
                templateUrl: '/static/partials/benefit_selection/tab_hsa.html',
                controller: 'hsaBenefitSignup'
            }).
            state('employee_benefit_signup.basic_life', {
                url: '/basic_life',
                templateUrl: '/static/partials/benefit_selection/tab_basic_life.html',
                controller:'basicLifeBenefitsSignup'
            }).
            state('employee_benefit_signup.supplemental_life', {
                url: '/supplemental_life',
                templateUrl: '/static/partials/benefit_selection/tab_supplemental_life.html',
                controller:'supplementalLifeBenefitsSignup'
            }).
            state('employee_benefit_signup.std', {
                url: '/std',
                templateUrl: '/static/partials/benefit_selection/tab_std.html',
                controller:'stdBenefitsSignup'
            }).
            state('employee_benefit_signup.ltd', {
                url: '/ltd',
                templateUrl: '/static/partials/benefit_selection/tab_ltd.html',
                controller:'ltdBenefitsSignup'
            }).
            state('employee_benefit_signup.hra', {
                url: '/hra',
                templateUrl: '/static/partials/benefit_selection/tab_hra.html',
                controller:'hraBenefitsSignup'
            }).
            state('employee_benefit_signup.commuter', {
                url: '/commuter',
                templateUrl: '/static/partials/benefit_selection/tab_commuter.html',
                controller:'commonBenefitsSignup'
            }).
            state('employee_benefit_signup.extra_benefit', {
                url: '/extra_benefit',
                templateUrl: '/static/partials/benefit_selection/tab_extra_benefit.html',
                controller:'commonBenefitsSignup'
            }).
            state('employee_benefit_signup.summary', {
                url: '/summary',
                templateUrl: '/static/partials/benefit_selection/tab_summary.html',
                controller:'benefitSignupSummary'
            }).
            state('employee_payroll', {
                url: '/employee/payroll',
                templateUrl: '/static/partials/payroll/main.html',
                controller: 'employeePayrollController'
            }).
            state('employee_payroll.w4', {
                url: '/w4',
                templateUrl: '/static/partials/payroll/tab_w4.html',
                controller: 'employeeW4Controller'
            }).
            state('employee_payroll.w4_edit', {
                url: '/edit',
                templateUrl: '/static/partials/payroll/tab_w4_edit.html',
                controller: 'employeeW4Controller'
            }).
            state('employee_payroll.direct_deposit', {
                url: '/direct_deposit',
                templateUrl: '/static/partials/payroll/tab_direct_deposit.html',
                controller: 'employeeDirectDepositController',
            }).
            state('employee_profile', {
                url: '/employee/profile',
                templateUrl: '/static/partials/employee_profile/main.html',
                controller: 'employeeProfileController'
            }).
            state('employee_profile.i9', {
                url: '/i9',
                templateUrl: '/static/partials/employee_profile/tab_i9.html',
                controller: 'employeeI9Controller'
            }).
            state('employee_profile.i9_edit', {
                url: '/i9/edit',
                templateUrl: '/static/partials/employee_profile/tab_i9_edit.html',
                controller: 'employeeI9Controller'
            }).
            state('employee_family', {
                url: '/employee/family/:employeeId?',
                templateUrl: '/static/partials/family_management/base.html',
                controller: 'employeeFamilyController'
            }).
            state('/employee/signup/:signup_number', {
                url: '/employee/signup/:signup_number',
                templateUrl: '/static/partials/employee_signup.html',
                controller: 'employeeSignup'
            }).
            state('/employee/document/:doc_id', {
                url: '/employee/document/:doc_id',
                templateUrl: '/static/partials/employee_view_document.html',
                controller: 'viewDocument'
            }).
            state('/employee/sign_letter/:employee_id', {
                url: '/employee/sign_letter/:employee_id?letter_type',
                templateUrl: '/static/partials/employee_onboard/employee_view_letter.html',
                controller: 'employeeAcceptDocument'
            }).
            state('employee_onboard', {
                url: '/employee/onboard/:employee_id',
                templateUrl: '/static/partials/employee_onboard/index.html',
                controller: 'onboardIndex'
            }).
            state('employee_onboard.basic_info', {
                url: '/basic_info',
                templateUrl: '/static/partials/employee_onboard/partial_basic_info.html',
                controller: 'onboardBasicInfo'
            }).
            state('employee_onboard.employment', {
                url: '/employment',
                templateUrl: '/static/partials/employee_onboard/partial_employment.html',
                controller: 'onboardEmployment'
            }).
            state('employee_onboard.tax', {
                url: '/tax',
                templateUrl: '/static/partials/employee_onboard/partial_tax.html',
                controller: 'onboardTax'
            }).
            state('employee_onboard.document', {
                url: '/document',
                templateUrl: '/static/partials/employee_onboard/partial_document.html',
                controller: 'onboardDocument'
            }).
            state('employee_onboard.direct_deposit', {
                url: '/direct_deposit',
                templateUrl: '/static/partials/employee_onboard/partial_direct_deposit.html',
                controller: 'onboardDirectDeposit'
            }).
            state('employeeUploads', {
                url:'/employee/uploads',
                templateUrl:'/static/partials/manage_uploads.html'
            }).
            state('employeeSupport', {
              url: '/employee/support',
              templateUrl: '/static/partials/help_center/employee_help_center.html',
              controller: 'employeeHelpCenterController'
            }).
            state('employeetimeoff', {
                url: '/employee/hr/timeoff',
                templateUrl: '/static/partials/timeoff/timeoff_base.html',
                controller: 'employeeViewTimeOffController'
            }).
            state('employee_timesheet', {
                url: '/employee/hr/work_timesheet',
                templateUrl: '/static/partials/work_timesheet/timesheet_base.html',
                controller: 'employeeViewWorkTimeSheetController'
            }).
            state('employee_timepunchcard',{
                url: '/employee/hr/timepunchcards',
                templateUrl: '/static/partials/time_punch_card/time_punch_card_base.html',
                controller: 'employeeManageTimePunchCardController'
            });
     }
 ]);

// Bootstrap the application
BenefitMyApp.run(function ($rootScope, LoggingService) {

    // Register the Logging Service to the $rootScope, so it
    // can be used by all controllers without explicit injection
    $rootScope.LoggingService = LoggingService;
});
