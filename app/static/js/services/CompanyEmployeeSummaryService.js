var benefitmyService = angular.module('benefitmyService');

var API_PREFIX = '/api/v1'

benefitmyService.factory('CompanyEmployeeSummaryService', [
  '$q',
  'employerWorkerRepository',
  function ($q, employerWorkerRepository){

    var mapToViewEmployeeList = function(domainList) {
      var viewList = [];

      _.each(domainList, function(employee) {
        var viewModel = {
          firstName: employee.user.first_name,
          lastName: employee.user.last_name,
          userId: employee.user.id,
          email: employee.user.email
        };
        viewList.push(viewModel);
      });

      return viewList;
    };

    var getCompanyEmployeeSummary = function(companyId) {
      var deferred = $q.defer();

      employerWorkerRepository.get({companyId: companyId}).$promise
      .then(function(response) {

        var users = response.user_roles;
        var employees = [];
        if (users) {
          employees = _.filter(users, function(user) {
            return user.company_user_type === 'employee';
          });
        }

        var mappedList = mapToViewEmployeeList(employees);
        deferred.resolve(mappedList);

      }, function(error) {
        deferred.reject(error);
      });

      return deferred.promise;
    };

    return {
      getCompanyEmployeeSummary: getCompanyEmployeeSummary,

      getCompanyEmployeeSummaryExcelUrl: function(companyId) {
        return API_PREFIX + '/companies/' + companyId + '/users/excel';
      },

      getCompanyEmployeeDirectDepositExcelUrl: function(companyId) {
        return API_PREFIX + '/companies/' + companyId + '/users/excel/direct_deposit'
      },

      getCompanyEmployeeLifeInsuranceBeneficiarySummaryExcelUrl: function(companyId) {
        return API_PREFIX + '/companies/' + companyId + '/users/excel/life_beneficiary';
      },

      getCompanyBenefitsBillingReportExcelUrl: function(companyId){
        return API_PREFIX + '/companies/' + companyId + '/users/excel/benefits_billing';
      },

      getCompanyEmployeeSummaryPdfUrl: function(companyId) {
        return API_PREFIX + '/companies/' + companyId + '/users/pdf';
      },

      getCompanyHphcExcelUrl: function(companyId) {
        return API_PREFIX + '/companies/' + companyId + '/hphc/excel';
      },

      getEmployee1095cUrl: function(employeeUserId) {
        return API_PREFIX + '/users/' + employeeUserId + '/forms/1095c';
      }
    };
  }
]);
