BenefitMyApp.controller('PeriodReportModalController', [
  '$scope',
  '$modalInstance',
  'AdvantagePayrollService',
  'companyId',
  function($scope,
           $modalInstance,
           AdvantagePayrollService,
           companyId){

    $scope.inputModel = {
        startDate: moment().format('M/D/YYYY'),
        endDate: moment().format('M/D/YYYY')
    };

    $scope.isValidToDownload = function() {
        var startDate = moment($scope.inputModel.startDate);
        var endDate = moment($scope.inputModel.endDate);
        return startDate.isValid()
            && endDate.isValid()
            && startDate <= endDate;
    };

    $scope.getDownloadLink = function() {
        return AdvantagePayrollService.getTimeTrackingReportCsvUrl(
            companyId,
            $scope.inputModel.startDate,
            $scope.inputModel.endDate
        );
    };

    $scope.close = function() {
        $modalInstance.close();
    };

    $scope.cancel = function() {
        $modalInstance.dismiss();
    };
  }
]).controller('AdvantagePayrollViewDirectiveController', [
  '$scope',
  '$state',
  '$modal',
  '$controller',
  'AdvantagePayrollService',
  function($scope,
           $state,
           $modal,
           $controller,
           AdvantagePayrollService) {

    // Inherite scope from base
    $controller('modalMessageControllerBase', {$scope: $scope});

    $scope.allEmployeesSetupCsvDownloadLink = AdvantagePayrollService.getAllEmployeesPayrollSertupDataCsvUrl($scope.companyId);
    
    $scope.openPeriodExportModal = function() {
        $modal.open({
            templateUrl: '/static/partials/payroll_integration/modal_advantage_payroll_period_export.html',
            controller: 'PeriodReportModalController',
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
]).directive('bmAdvantagePayrollView', function(){

    return {
        restrict: 'E',
        scope: {
          companyId: '='        
        },
        templateUrl: '/static/partials/payroll_integration/directive_advantage_payroll_view.html',
        controller: 'AdvantagePayrollViewDirectiveController'
      };
});