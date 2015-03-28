var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory(
  'CompanyEmployeeSummaryService', 
  [
  function (){
    return {
      getCompanyEmployeeSummaryExcelUrl: function(companyId) {
        return '/api/v1/companies/' + companyId + '/users/excel';
      },

      getCompanyEmployeeLifeInsuranceBeneficiarySummaryExcelUrl: function(companyId) {
        return '/api/v1/companies/' + companyId + '/users/excel/life_beneficiary';
      }
    }; 
  }
]);
