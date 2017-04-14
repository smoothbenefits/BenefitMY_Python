var benefitmyService = angular.module('benefitmyService');

var API_PREFIX = '/api/v1'
var API_PREFIX_V2 = '/api/v2'

benefitmyService.factory('AdvantagePayrollService', [
  '$q',
  function ($q){

    return {

      getAllEmployeesPayrollSertupDataCsvUrl: function(companyId) {
        return API_PREFIX + '/companies/' + companyId + '/advantage_payroll/setup_csv';
      },

      getTimeTrackingReportCsvUrl: function(companyId, startDate, endDate) {
        var reportUrl = API_PREFIX + '/companies/' + companyId + '/advantage_payroll/period_export_csv';
        reportUrl += '/from' + moment(startDate).format('/YYYY/M/DD');
        reportUrl += '/to' + moment(endDate).format('/YYYY/M/DD');
        return reportUrl;
      }

    };
  }
]);
