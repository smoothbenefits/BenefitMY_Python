BenefitMyApp.directive('bmStateTaxElectionView', function() {

    var StateTaxElectionEditModalController = [
       '$scope',
       '$state',
       '$modalInstance',
       '$q',
       'EmployeeTaxElectionService',
       'taxElection',
       'userId',
        function(
            $scope,
            $state,
            $modalInstance,
            $q,
            EmployeeTaxElectionService,
            taxElection,
            userId) {

            // Whether we are in create or edit mode is determined by whether the modal
            // was given an existing tax election to edit.
            $scope.isCreateMode = !taxElection;

            if (taxElection) {
                $scope.taxElection = angular.copy(taxElection);
            } else {
                $scope.taxElection = EmployeeTaxElectionService.getBlankElection(userId, 'MA');
            }

            $scope.isValidToSave = function() {
                return EmployeeTaxElectionService.isValidTaxElection($scope.taxElection);
            };

            $scope.cancel = function() {
                $modalInstance.dismiss('cancelByUser');
            };

            $scope.save = function() {
                EmployeeTaxElectionService.saveTaxElection($scope.taxElection).then(function(savedElection) {
                    $modalInstance.close({ success: true, data: savedElection });
                }, function(error) {
                    $modalInstance.close({ success: false, data: error });
                });
            };
        }
    ];

    var StateTaxElectionViewDirectiveController = [
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

        $scope.editElection = function(election) {
          var modalInstance = $modal.open({
            templateUrl: '/static/partials/tax/modal_edit_state_tax_election.html',
            controller: StateTaxElectionEditModalController,
            size: 'lg',
            backdrop: 'static',
            resolve: {
              taxElection: function () {
                return election;
              },
              userId: function() {
                return $scope.userId;
              }
            }
          });

          modalInstance.result.then(function(result){
            if (result.success) {
                var successMessage = "State tax election has been successfully saved!";
                $scope.showMessageWithOkayOnly('Success', successMessage);
                
                // Refresh the set of elections from server
                EmployeeTaxElectionService.getTaxElectionsByEmployee(userId).then(function(elections){
                    $scope.elections = elections;
                });
            } else {
                var failureMessage = "Failed to save state tax election. Message: " + result.data;
                $scope.showMessageWithOkayOnly('Failed', failureMessage);
            }
          });
        };

      }
    ];

    return {
        restrict: 'E',
        scope: { 
            userId: '='     
        },
        templateUrl: '/static/partials/tax/directive_state_tax_election_view.html',
        controller: StateTaxElectionViewDirectiveController
    };
});