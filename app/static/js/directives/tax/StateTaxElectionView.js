BenefitMyApp.directive('bmStateTaxElectionView', function() {

    var stateElectionFormTemplateUrlMapping = {
        'MA': '/static/partials/tax/state_tax_election_form_MA.html',
        'RI': '/static/partials/tax/state_tax_election_form_RI.html'
    };

    var StateSelectionModalController = [
       '$scope',
       '$state',
       '$modalInstance',
       '$q',
       'statesYetElected',
        function(
            $scope,
            $state,
            $modalInstance,
            $q,
            statesYetElected) {

            $scope.statesYetElected = statesYetElected;
            $scope.selectedState = statesYetElected[0];

            $scope.cancel = function() {
                $modalInstance.dismiss('cancelByUser');
            };

            $scope.ok = function() {
                $modalInstance.close($scope.selectedState);
            };
        }
    ];

    var StateTaxElectionEditModalController = [
       '$scope',
       '$state',
       '$modalInstance',
       '$q',
       'EmployeeTaxElectionService',
       'taxElection',
        function(
            $scope,
            $state,
            $modalInstance,
            $q,
            EmployeeTaxElectionService,
            taxElection) {

            if (taxElection) {
                $scope.taxElection = angular.copy(taxElection);
            }

            $scope.stateElectionFormTemplateUrl = function() {
                return stateElectionFormTemplateUrlMapping[$scope.taxElection.state];
            };

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

        var refreshCurrentElections = function() {
            EmployeeTaxElectionService.getTaxElectionsByEmployee($scope.userId).then(function(elections){
                $scope.elections = elections;
            });
        };

        $scope.$watch('userId', function(userId) {
            if (userId) {
                refreshCurrentElections();
            }
        });

        var getStatesYetElected = function() {
            var existingStates = _.map($scope.elections, function(election) {
                return election.state;
            });

            return _.reject(EmployeeTaxElectionService.TaxElectionSupportedStates, function(state) {
                return _.contains(existingStates, state);
            });
        };

        $scope.canCreateNewElection = function() {
            var statesYetElected = getStatesYetElected();
            return statesYetElected && statesYetElected.length > 0;
        };

        $scope.hasExistingElections = function() {
            return $scope.elections && $scope.elections.length > 0;
        };

        $scope.createElection = function() {
            var modalInstance = $modal.open({
            templateUrl: '/static/partials/tax/modal_state_selection.html',
            controller: StateSelectionModalController,
            size: 'sm',
            backdrop: 'static',
            resolve: {
              statesYetElected: function() {
                return getStatesYetElected();
              }
            }
          });

          modalInstance.result.then(function(selectedState){
            // Construct a blank election based on the state selected
            var blankElection = EmployeeTaxElectionService.getBlankElection($scope.userId, selectedState);
            $scope.editElection(blankElection);
          });
        };

        $scope.editElection = function(election) {
          var modalInstance = $modal.open({
            templateUrl: '/static/partials/tax/modal_edit_state_tax_election.html',
            controller: StateTaxElectionEditModalController,
            size: 'lg',
            backdrop: 'static',
            resolve: {
              taxElection: function () {
                return election;
              }
            }
          });

          modalInstance.result.then(function(result){
            if (result.success) {
                var successMessage = "State tax election has been successfully saved!";
                $scope.showMessageWithOkayOnly('Success', successMessage);
                
                // Refresh the set of elections from server
                refreshCurrentElections();
            } else {
                var failureMessage = "Failed to save state tax election. Message: " + result.data;
                $scope.showMessageWithOkayOnly('Failed', failureMessage);
            }
          });
        };

        $scope.deleteElection = function(election) {
            EmployeeTaxElectionService.deleteTaxElection(election).then(
                function() {
                    // Refresh the set of elections from server
                    refreshCurrentElections();
                },
                function(errors) {
                    var failureMessage = "Failed to delete state tax election. Message: " + errors;
                    $scope.showMessageWithOkayOnly('Failed', failureMessage);
                }
            );
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