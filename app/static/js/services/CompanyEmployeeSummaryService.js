var benefitmyService = angular.module('benefitmyService');

var API_PREFIX = '/api/v1'

benefitmyService.factory(
  'CompanyEmployeeSummaryService', 
  [
  function (){
    return {
      getCompanyEmployeeSummaryExcelUrl: function(companyId) {
        return API_PREFIX + '/companies/' + companyId + '/users/excel';
      },

      getCompanyEmployeeDirectDepositExcelUrl: function(companyId) {
        return API_PREFIX + '/companies/' + companyId + '/users/excel/direct_deposit'
      },

      getCompanyEmployeeLifeInsuranceBeneficiarySummaryExcelUrl: function(companyId) {
        return API_PREFIX + '/companies/' + companyId + '/users/excel/life_beneficiary';
      },

      getCompanyBenefitsFinancialReportExcelUrl: function(companyId){
        return API_PREFIX + '/companies/' + companyId + '/users/excel/benefits_financial';
      }
    }; 
  }
]);
