BenefitMyApp.controller('StateTaxElectionViewDirectiveController', [
  '$scope',
  '$state',
  '$modal',
  '$controller',
  function($scope,
           $state,
           $modal,
           $controller) {

    // Inherite scope from base
    $controller('modalMessageControllerBase', {$scope: $scope});
  }
]).directive('bmStateTaxElectionView', function(){

    return {
        restrict: 'E',
        scope: {      
        },
        templateUrl: '/static/partials/tax/directive_state_tax_election_view.html',
        controller: 'StateTaxElectionViewDirectiveController'
      };
});