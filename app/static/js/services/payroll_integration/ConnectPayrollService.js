var benefitmyService = angular.module('benefitmyService');

var API_PREFIX = '/api/v1'

benefitmyService.factory('ConnectPayrollService', [
  '$q',
  function ($q){

    return {

      getAllEmployeesFrontPageCsvUrl: function(companyId) {
        return API_PREFIX + '/companies/' + companyId + '/connect_payroll/employee_frontpage_csv';
      },

      getTimeTrackingReportCsvUrl: function(companyId, startDate, endDate) {
        var reportUrl = API_PREFIX + '/companies/' + companyId + '/connect_payroll/period_export_csv';
        reportUrl += '/from' + moment(startDate).format('/YYYY/M/DD');
        reportUrl += '/to' + moment(endDate).format('/YYYY/M/DD');
        return reportUrl;
      }

    };
  }
]);
