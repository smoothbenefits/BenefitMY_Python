BenefitMyApp.controller('AdvantagePayrollViewDirectiveController', [
  '$scope',
  '$state',
  '$modal',
  '$controller',
  function($scope,
           $state,
           $modal,
           $controller){

    // Inherite scope from base
    $controller('modalMessageControllerBase', {$scope: $scope});

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