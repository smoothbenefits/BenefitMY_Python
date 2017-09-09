BenefitMyApp.controller('StateTaxElectionViewDirectiveController', [
  '$scope',
  '$state',
  '$modal',
  '$controller',
  'EmployeeTaxElectionService',
  function($scope,
           $state,
           $modal,
           $controller,
           EmployeeTaxElectionService) {

    // Inherite scope from base
    $controller('modalMessageControllerBase', {$scope: $scope});

    $scope.$watch('userId', function(userId) {
        if (userId) {
            EmployeeTaxElectionService.getTaxElectionsByEmployee(userId).then(function(elections){
                $scope.elections = elections;
            });
        }
    });
  }
]).directive('bmStateTaxElectionView', function(){

    return {
        restrict: 'E',
        scope: { 
            userId: '='     
        },
        templateUrl: '/static/partials/tax/directive_state_tax_election_view.html',
        controller: 'StateTaxElectionViewDirectiveController'
      };
});