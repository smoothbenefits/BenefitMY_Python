var BenefitMyApp = angular.module('BenefitMyApp',[
    'ngRoute',
    'ui.mask',
    'benefitmyService',
    'benefitmyApp.brokers.controllers',
    'benefitmyApp.employers.controllers',
    'benefitmyApp.employees.controllers']);

//Setup underscore:

var underscore = angular.module('underscore', []);
underscore.factory('_', function(){
    return window._;
});

BenefitMyApp.config(['$routeProvider',
    function ($routeProvider) {
        $routeProvider.
            when('/broker', {
                 templateUrl: 'partials/clients.html',
                 controller: 'clientsController'
             }).
            when('/add_client', {
                 templateUrl: 'partials/add_client.html',
                 controller: 'addClientController'
             }).
            when('/benefits/:clientId', {
                templateUrl: 'partials/company_benefits.html',
                controller: 'benefitsController'
            }).
            when('/add_benefit/:clientId', {
                templateUrl: 'partials/add_benefit.html',
                controller: 'addBenefitController'
            }).
            when('/', {
                template: '',
                controller:'findViewController'
            }).
            when('/admin',{
                templateUrl: 'partials/employer_dashboard.html',
                controller: 'employerHome'
            }).
            when('/admin/broker/add/:company_id', {
                templateUrl:'partials/add_broker.html',
                controller:'employerUser'
            }).
            when('/admin/broker/:company_id', {
                templateUrl:'partials/view_broker.html',
                controller:'employerUser'
            }).
            when('/admin/benefits/:company_id', {
                templateUrl:'partials/employer_view_benefits.html',
                controller:'employerBenefits'
            }).
            when('/admin/employee/add/:company_id', {
                templateUrl:'partials/add_employee.html',
                controller:'employerUser'
            }).
            when('/admin/employee/:company_id', {
                templateUrl:'partials/view_employee.html',
                controller:'employerUser'
            }).
            when('/admin/generate_template/:company_id', {
                templateUrl:'partials/template.html',
                controller:'employerLetterTemplate'
            }).
            when('/admin/create_letter/:company_id/:employee_id', {
                templateUrl:'/partials/create_letter.html',
                controller:'employerCreateLetter'
            }).
            when('/admin/view_letter/:company_id/:employee_id', {
                templateUrl:'/partials/view_letter.html',
                controller:'employerViewLetter'
            }).
            when('/employee',{
                templateUrl: 'partials/employee_dashboard.html',
                controller: 'employeeHome'
            }).
            when('/employee/benefit/:employee_id', {
                templateUrl: 'partials/employee_benefits.html',
                controller:'employeeBenefitSignup'
            }).
            when('/employee/family/:employee_id', {
                templateUrl: 'partials/employee_family.html',
                controller: 'employeeFamily'
            }).
            when('/employee/signin/:employee_id', {
                templateUrl: 'partials/employee_signin.html',
                controller: 'employeeSignin'
            }).
            when('/employee/signup/:signup_number', {
                templateUrl: 'partials/employee_signup.html',
                controller: 'employeeSignup'
            }).
            when('/add_family/:employee_id', {
                templateUrl: 'partials/add_family.html',
                controller: 'addFamily'
            }).
            when('/employee/document/:doc_id', {
                templateUrl: 'partials/employee_view_document.html',
                controller: 'viewDocument'
            }).
            when('/employee/onboard/index/:employee_id', {
                templateUrl: 'partials/employee_onboard/index.html',
                controller: 'onboardIndex'
            }).
            when('/employee/onboard/employment/:employee_id', {
                templateUrl: 'partials/employee_onboard/employment.html',
                controller: 'onboardEmployment'
            }).
            when('/employee/onboard/tax/:employee_id', {
                templateUrl: 'partials/employee_onboard/tax.html',
                controller: 'onboardTax'
            }).
            when('/employee/onboard/complete/:employee_id', {
                templateUrl: 'partials/employee_onboard/complete.html',
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
