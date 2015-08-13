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

      getCompanyBenefitsBillingReportExcelUrl: function(companyId){
        return API_PREFIX + '/companies/' + companyId + '/users/excel/benefits_billing';
      },

      getCompanyEmployeeSummaryPdfUrl: function(companyId) {
        return API_PREFIX + '/companies/' + companyId + '/users/pdf';
      },

      getCompanyHphcExcelUrl: function(companyId) {
        return API_PREFIX + '/companies/' + companyId + '/hphc/excel';
      }
    };
  }
]);
