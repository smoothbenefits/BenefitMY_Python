var benefitmyService = angular.module('benefitmyService');

var API_PREFIX = '/api/v1'

benefitmyService.factory('ConnectPayrollService', [
  '$q',
  function ($q){

    return {

      getTimeTrackingReportCsvUrl: function(companyId, startDate, endDate) {
        var reportUrl = API_PREFIX + '/companies/' + companyId + '/connect_payroll/period_export_csv';
        reportUrl += '/from' + moment(startDate).format('/YYYY/M/DD');
        reportUrl += '/to' + moment(endDate).format('/YYYY/M/DD');
        return reportUrl;
      }

    };
  }
]);
