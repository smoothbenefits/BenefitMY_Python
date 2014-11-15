var BenefitMyApp = angular.module('BenefitMyApp',[
    'ngRoute',
    'ngResource',
    'ui.mask',
    'benefitmyService',
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
}

BenefitMyApp.config(['$resourceProvider', '$httpProvider', function($resourceProvider, $httpProvider) {
  // Don't strip trailing slashes from calculated URLs
  $resourceProvider.defaults.stripTrailingSlashes = false;

  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

BenefitMyApp.config(['$routeProvider',
    function ($routeProvider) {
        $routeProvider.
            when('/broker', {
                 templateUrl: '/static/partials/clients.html',
                 controller: 'clientsController'
             }).
            when('/broker/add_client', {
                 templateUrl: '/static/partials/add_client.html',
                 controller: 'addClientController'
             }).
            when('/broker/benefits/:clientId', {
                templateUrl: '/static/partials/company_benefits.html',
                controller: 'benefitsController'
            }).
            when('/broker/add_benefit/:clientId', {
                templateUrl: '/static/partials/add_benefit.html',
                controller: 'addBenefitController'
            }).
            when('/', {
                template: '',
                controller:'findViewController'
            }).
            when('/admin',{
                templateUrl: '/static/partials/employer_dashboard.html',
                controller: 'employerHome'
            }).
            when('/admin/broker/add/:company_id', {
                templateUrl:'/static/partials/add_broker.html',
                controller:'employerUser'
            }).
            when('/admin/broker/:company_id', {
                templateUrl:'/static/partials/view_broker.html',
                controller:'employerUser'
            }).
            when('/admin/benefits/:company_id', {
                templateUrl:'/static/partials/employer_view_benefits.html',
                controller:'employerBenefits'
            }).
            when('/admin/employee/add/:company_id', {
                templateUrl:'/static/partials/add_employee.html',
                controller:'employerUser'
            }).
            when('/admin/employee/:company_id', {
                templateUrl:'/static/partials/view_employee.html',
                controller:'employerUser'
            }).
            when('/admin/generate_template/:company_id', {
                templateUrl:'/static/partials/template.html',
                controller:'employerLetterTemplate'
            }).
            when('/admin/create_letter/:company_id/:employee_id', {
                templateUrl:'/static/partials/create_letter.html',
                controller:'employerCreateLetter'
            }).
            when('/admin/view_letter/:company_id/:employee_id', {
                templateUrl:'/static/partials/view_letter.html',
                controller:'employerViewLetter'
            }).
            when('/admin/view_draft/:company_id/:employee_id/:document_type_id', {
                templateUrl: '/static/partials/view_draft.html',
                controller: 'employerViewDraft'
            }).
            when('/employee',{
                templateUrl: '/static/partials/employee_dashboard.html',
                controller: 'employeeHome'
            }).
            when('/employee/benefit/:employee_id', {
                templateUrl: '/static/partials/employee_benefits.html',
                controller:'employeeBenefitSignup'
            }).
            when('/employee/family/:employee_id', {
                templateUrl: '/static/partials/employee_family.html',
                controller: 'employeeFamily'
            }).
            when('/employee/signup/:signup_number', {
                templateUrl: '/static/partials/employee_signup.html',
                controller: 'employeeSignup'
            }).
            when('/employee/add_family/:employee_id', {
                templateUrl: '/static/partials/add_family.html',
                controller: 'addFamily'
            }).
            when('/employee/document/:doc_id', {
                templateUrl: '/static/partials/employee_view_document.html',
                controller: 'viewDocument'
            }).
            when('/employee/onboard/index/:employee_id', {
                templateUrl: '/static/partials/employee_onboard/index.html',
                controller: 'onboardIndex'
            }).
            when('/employee/onboard/employment/:employee_id', {
                templateUrl: '/static/partials/employee_onboard/employment.html',
                controller: 'onboardEmployment'
            }).
            when('/employee/onboard/tax/:employee_id', {
                templateUrl: '/static/partials/employee_onboard/tax.html',
                controller: 'onboardTax'
            }).
            when('/employee/onboard/complete/:employee_id', {
                templateUrl: '/static/partials/employee_onboard/complete.html',
                controller: 'onboardComplete'
            }).
            otherwise({
                redirectTo:'/'
            });
     }
 ]);

String.prototype.capitalize = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
}
