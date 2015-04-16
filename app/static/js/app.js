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

BenefitMyApp.config(['$resourceProvider', '$httpProvider', function($resourceProvider, $httpProvider) {
  // Don't strip trailing slashes from calculated URLs
  $resourceProvider.defaults.stripTrailingSlashes = false;

  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

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
            state('employee_benefit_signup.optional_life', {
                url: '/basic_life',
                templateUrl: '/static/partials/benefit_selection/tab_optional_life.html',
                controller:'optionalLifeBenefitsSignup'
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
            state('/employee/family/:employee_id', {
                url: '/employee/family/:employee_id',
                templateUrl: '/static/partials/employee_family.html',
                controller: 'employeeFamily'
            }).
            state('/employee/signup/:signup_number', {
                url: '/employee/signup/:signup_number',
                templateUrl: '/static/partials/employee_signup.html',
                controller: 'employeeSignup'
            }).
            state('/employee/add_family/:employee_id', {
                url: '/employee/add_family/:employee_id',
                templateUrl: '/static/partials/add_family.html',
                controller: 'addFamily'
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
                templateUrl:'/static/partials/manage_uploads.html',
                controller: 'manageUploadController'
            });
     }
 ]);