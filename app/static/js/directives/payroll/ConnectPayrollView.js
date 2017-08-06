BenefitMyApp.controller('CPPeriodReportModalController', [
  '$scope',
  '$modalInstance',
  'ConnectPayrollService',
  'CompanyService',
  'DateTimeService',
  'companyId',
  function($scope,
           $modalInstance,
           ConnectPayrollService,
           CompanyService,
           DateTimeService,
           companyId){

    $scope.inputModel = {
        startDate: moment().format('M/D/YYYY'),
        endDate: moment().format('M/D/YYYY')
    };

    CompanyService.getCompanyInfo(companyId).then(function(companyInfo) {
        var payPeriodName = companyInfo.payPeriod.name;
        if (payPeriodName.toLowerCase().indexOf('week') >= 0) {
            // The pay period is by number of weeks and hence
            // we should be able to assume the time range should
            // normally be on week boundary
            $scope.expectWeekBoundary = true;
            var weekBoundary = DateTimeService.GetWeekBoundary(moment());
            $scope.inputModel.startDate = weekBoundary.startDateOfWeek.format('M/D/YYYY');
            $scope.inputModel.endDate = weekBoundary.endDateOfWeek.format('M/D/YYYY');
        }
    });

    $scope.isValidToDownload = function() {
        var startDate = moment($scope.inputModel.startDate);
        var endDate = moment($scope.inputModel.endDate);
        return startDate.isValid()
            && endDate.isValid()
            && startDate <= endDate;
    };

    $scope.getDownloadLink = function() {
        return ConnectPayrollService.getTimeTrackingReportCsvUrl(
            companyId,
            $scope.inputModel.startDate,
            $scope.inputModel.endDate
        );
    };

    $scope.validateWeekBoundaryForStartDate = function() {
        if ($scope.expectWeekBoundary) {
            var startDate = moment($scope.inputModel.startDate);

            return DateTimeService.IsWeekStart(startDate);
        }

        return true;
    };

    $scope.validateWeekBoundaryForEndDate = function() {
        if ($scope.expectWeekBoundary) {
            var endDate = moment($scope.inputModel.endDate);

            return DateTimeService.IsWeekEnd(endDate);
        }

        return true;
    };

    $scope.getCorrectedStartDateForDisplay = function() {
        var startDate = moment($scope.inputModel.startDate);
        var weekBoundary = DateTimeService.GetWeekBoundary(startDate);
        return weekBoundary.startDateOfWeek.format('M/D/YYYY');
    };

    $scope.getCorrectedEndDateForDisplay = function() {
        var endDate = moment($scope.inputModel.endDate);
        var weekBoundary = DateTimeService.GetWeekBoundary(endDate);
        return weekBoundary.endDateOfWeek.format('M/D/YYYY');
    };

    $scope.close = function() {
        $modalInstance.close();
    };

    $scope.cancel = function() {
        $modalInstance.dismiss();
    };
  }
]).controller('ConnectPayrollViewDirectiveController', [
  '$scope',
  '$state',
  '$modal',
  '$controller',
  'ConnectPayrollService',
  function($scope,
           $state,
           $modal,
           $controller,
           ConnectPayrollService) {

    // Inherite scope from base
    $controller('modalMessageControllerBase', {$scope: $scope});

    $scope.openPeriodExportModal = function() {
        $modal.open({
            templateUrl: '/static/partials/payroll_integration/modal_connect_payroll_period_export.html',
            controller: 'CPPeriodReportModalController',
            backdrop: 'static',
            size: 'md',
            resolve: {
                companyId: function() {
                    return $scope.companyId;
                }
            }
        });
    };
  }
]).directive('bmConnectPayrollView', function(){

    return {
        restrict: 'E',
        scope: {
          companyId: '='        
        },
        templateUrl: '/static/partials/payroll_integration/directive_connect_payroll_view.html',
        controller: 'ConnectPayrollViewDirectiveController'
      };
});