BenefitMyApp.controller('TimesheetReportDownloadViewDirectiveController', [
  '$scope', '$modal', function($scope, $modal) {
    $scope.downloadWeeklyTimeSheetReport = function() {
      var modalInstance = $modal.open({
        templateUrl: '/static/partials/common/modal_download_work_time_report.html',
        controller: 'TimesheetReportDownloadModalController',
        size: 'md',
        backdrop: 'static',
        resolve: {
          'selectedDisplayWeek': function() {
            return $scope.week;
          },
          'companyId': function() {
            return $scope.company.id;
          }
        }
      });
    };
  }
]).controller('TimesheetReportDownloadModalController', [
  '$scope', '$modalInstance', 'CompanyEmployeeSummaryService', 'selectedDisplayWeek', 'companyId',
  function($scope, $modalInstance, CompanyEmployeeSummaryService, selectedDisplayWeek, companyId) {

    $scope.downloadType = 'current';

    $scope.showWeekSelector = function() {
      return $scope.downloadType === 'custom';
    };

    $scope.download = function(){

      if ($scope.report.starting_date > $scope.report.end_date) {
        $scope.warningMessage = 'End date must not be earlier than start date.';
        return;
      }

      if (($scope.report.starting_date && !$scope.report.end_date) ||
      (!$scope.report.starting_date && $scope.report.end_date)) {
        $scope.warningMessage = 'Both start date and end date are needed.';
        return;
      }

      // Convert to the start date of the week selected
      var start_week_start_date, end_week_start_date;
      if ($scope.showWeekSelector()) {
        start_week_start_date = moment($scope.report.starting_date).startOf('week');
        end_week_start_date = moment($scope.report.end_date).startOf('week');
      } else {
        start_week_start_date = selectedDisplayWeek.weekStartDate;
        end_week_start_date = selectedDisplayWeek.weekStartDate;
      }

      var link = CompanyEmployeeSummaryService.getWeeklyWorktimeReportUrl(
        companyId,
        start_week_start_date,
        end_week_start_date);

      location.href = link;

      $modalInstance.close();
    };

    $scope.cancel = function() {
      $modalInstance.dismiss();
    };
  }
]).directive('bmTimesheetDownloadView', function() {
  return {
    restrict: 'E',
    scope: {
        text: '=',
        week: '=',
        company: '='
    },
    templateUrl: '/static/partials/common/directive_timesheet_report_download_view.html',
    controller: 'TimesheetReportDownloadViewDirectiveController'
  };
});
