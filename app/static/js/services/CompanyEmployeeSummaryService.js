var benefitmyService = angular.module('benefitmyService');

var API_PREFIX = '/api/v1'

benefitmyService.factory('CompanyEmployeeSummaryService', [
  '$q',
  'CompanyPersonnelsService',
  function ($q, CompanyPersonnelsService){

    var mapToViewEmployeeList = function(domainList) {
      var viewList = [];

      _.each(domainList, function(employee) {
        var viewModel = {
          firstName: employee.user.first_name,
          lastName: employee.user.last_name,
          userId: employee.user.id,
          email: employee.user.email,
          company_group_member: employee.company_group_member
        };
        viewList.push(viewModel);
      });

      return viewList;
    };

    var getCompanyEmployeeSummary = function(companyId) {
      return CompanyPersonnelsService.getCompanyEmployees(companyId)
      .then(function(employees){
        var mappedList = mapToViewEmployeeList(employees);
        return mappedList
      }, function(error) {
        deferred.reject(error);
      });
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
      },

      getWeeklyWorktimeReportUrl: function(companyId, weekStartDate){
        var reportUrl = API_PREFIX + '/company/' + companyId + '/worktime_excel';
        reportUrl += moment(weekStartDate).format('/YYYY/M/DD');
        return reportUrl;
      }
    };
  }
]);
