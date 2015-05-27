var BenefitMyApp = angular.module('BenefitMyApp',[
    'ngResource',
    'ui.router',
    'ui.mask',
    'ui.utils.masks',
    'ui.bootstrap',
    'angularFileUpload',
    'benefitmyDomainModelFactories',
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
var STORAGE_DATE_FORMAT_STRING = 'YYYY-MM-DD';

// The URL to which logging to server side should be posted to
var LOGGING_SERVER_URL = 'http://localhost:3999/api/bm_log' 

BenefitMyApp.config(['$resourceProvider', '$httpProvider', function($resourceProvider, $httpProvider) {
  // Don't strip trailing slashes from calculated URLs
  $resourceProvider.defaults.stripTrailingSlashes = false;

  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

// Configure global error logging
// - Preserves the default local logging to console
// - Add logging to server 
BenefitMyApp.config(function ($provide) {
  $provide.decorator("$exceptionHandler", 
    ['$delegate', '$window', '$log', 'BrowserDetectionService',  
    function($delegate, $window, $log, BrowserDetectionService) {
    return function (exception, cause) {
        // now try to log the error to the server side. 
        try {
            var errorMessage = exception.toString(); 

            // use our traceService to generate a stack trace 
            var stackTrace = printStackTrace({e: exception}); 

            // use AJAX (in this example jQuery) and NOT 
            // an angular service such as $http 
            $.ajax({ 
                type: "POST", 
                url: LOGGING_SERVER_URL, 
                contentType: "application/json", 
                data: angular.toJson({ 
                    url: $window.location.href, 
                    message: errorMessage,
                    browser: BrowserDetectionService.getBrowserBrand(), 
                    type: "exception", 
                    stackTrace: stackTrace.join('\n\n')}) })
            .fail(function(jqXHR, textStatus, errorThrown) {
                $log.warn("Error server-side logging failed");
                $log.log(errorThrown);
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

BenefitMyApp.config(['$stateProvider', '$urlRouterProvider',
    function ($stateProvider, $urlRouterProvider) {
        // For any unmatched url, redirect to state "/"
        $urlRouterProvider.otherwise("/");    

        $stateProvider.
            state('/settings', {
                url: "/settings?forced",
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
                templateUrl: '/static/partials/add_client.html',
                controller: 'addClientController'
            }).
            state('/broker/benefits/:clientId', {
                url: '/broker/benefits/:clientId',
                templateUrl: '/static/partials/view_benefits.html',
                controller: 'benefitsController'
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
            state('broker_add_benefit.hra', {
                url: '/hra',
                templateUrl: '/static/partials/benefit_addition/tab_hra.html',
                controller: 'brokerAddHraPlanController'
            }).
            state('/broker/benefit/selected/:client_id', {
                url: '/broker/benefit/selected/:client_id',
                templateUrl: '/static/partials/selected_benefits_company.html',
                controller: 'selectedBenefitsController'
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
            state('/admin/employee/:company_id', {
                url: '/admin/employee/:company_id',
                templateUrl:'/static/partials/view_employee.html',
                controller:'employerUser'
            }).
            state('/admin/generate_template/:company_id', {
                url: '/admin/generate_template/:company_id?type&add',
                templateUrl:'/static/partials/template.html',
                controller:'employerLetterTemplate'
            }).
            state('/admin/create_letter/:company_id/:employee_id', {
                url: '/admin/create_letter/:company_id/:employee_id?type',
                templateUrl:'/static/partials/create_letter.html',
                controller:'employerCreateLetter'
            }).
            state('/admin/view_letter/:company_id/:employee_id', {
                url: '/admin/view_letter/:company_id/:employee_id?type',
                templateUrl:'/static/partials/view_letter.html',
                controller:'employerViewLetter'
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
            state('/admin/benefit/election/:company_id',{
                url: '/admin/benefit/election/:company_id',
                templateUrl:'/static/partials/selected_benefits_company.html',
                controller: 'employerBenefitsSelected'
            }).
            state('admin_employee_uploads',{
                url: '/admin/:company_id/employee/:employee_id/uploads',
                templateUrl: '/static/partials/view_employee_uploads.html',
                controller: 'employerViewUploads'
            }).
            state('/employee',{
                url: '/employee',
                templateUrl: '/static/partials/employee_dashboard.html',
                controller: 'employeeHome'
            }).
            state('employee_benefit_signup', {
                url: '/employee/benefits/:employee_id',
                templateUrl: '/static/partials/benefit_selection/main.html',
                controller:'employeeBenefitsSignup'
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
                url: '/employee/family/:employeeId',
                templateUrl: '/static/partials/family_management/main.html',
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
            state('/employee/onboard/index/:employee_id', {
                url: '/employee/onboard/index/:employee_id',
                templateUrl: '/static/partials/employee_onboard/index.html',
                controller: 'onboardIndex'
            }).
            state('/employee/onboard/employment/:employee_id', {
                url: '/employee/onboard/employment/:employee_id',
                templateUrl: '/static/partials/employee_onboard/employment.html',
                controller: 'onboardEmployment'
            }).
            state('/employee/onboard/tax/:employee_id', {
                url: '/employee/onboard/tax/:employee_id',
                templateUrl: '/static/partials/employee_onboard/tax.html',
                controller: 'onboardTax'
            }).
            state('/employee/onboard/complete/:employee_id', {
                url: '/employee/onboard/complete/:employee_id',
                templateUrl: '/static/partials/employee_onboard/complete.html',
                controller: 'onboardComplete'
            }).
            state('employeeUploads', {
                url:'/employee/uploads',
                templateUrl:'/static/partials/manage_uploads.html'            
            });
     }
 ]);

// Bootstrap the application
BenefitMyApp.run(function ($rootScope, LoggingService) {

    // Register the Logging Service to the $rootScope, so it
    // can be used by all controllers without explicit injection
    $rootScope.LoggingService = LoggingService;
});
