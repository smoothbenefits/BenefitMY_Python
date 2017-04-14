BenefitMyApp.controller('EmployeePhraseologyModalController', [
  '$scope',
  '$modalInstance',
  'WorkersCompService',
  'companyPhraseologies',
  'employeePersonId',
  'employeePhraseology',
  function($scope,
           $modalInstance,
           WorkersCompService,
           companyPhraseologies,
           employeePersonId,
           employeePhraseology){

    $scope.modalHeader = 'Change Employee Phraseology Assignment';

    // Set the model object in focus
    // For now, we only allow reassignment. i.e. create new
    // records and not update existing ones
    $scope.contextEmployeePhraseology = WorkersCompService.GetBlankEmployeePhraseologyByEmployeePerson(employeePersonId);

    $scope.companyPhraseologies = companyPhraseologies;

    if (employeePhraseology) {
        // Find the phraseology from the company phraseologies dropdown
        // This is the workaround to get the dropdown selection
        // properly initialized. Due to Angular not working properly
        // when select as and track by used together.
        var currentPhraseology = _.find($scope.companyPhraseologies, function(phraseology) {
            return phraseology.phraseology.id == employeePhraseology.phraseology.id;
        });

        $scope.contextEmployeePhraseology.phraseology = currentPhraseology.phraseology;
    }

    $scope.cancel = function() {
        $modalInstance.dismiss();
    };

    $scope.save = function() {
        WorkersCompService.SaveEmployeePhraseology($scope.contextEmployeePhraseology).then(
            function(resultEmployeePhraseology) {
                var resultCopy = angular.copy(resultEmployeePhraseology);
                $modalInstance.close(resultCopy);
            },
            function(errors) {
                $modalInstance.close(null);
            }
        );
    }

    // Check whether the current state is valid for saving.
    //
    $scope.isValidToSave = function() {
        return !$scope.form.$invalid
            && $scope.contextEmployeePhraseology
            && $scope.contextEmployeePhraseology.phraseology
            && $scope.contextEmployeePhraseology.phraseology.id;
    };
  }
]).controller('EmployeePhraseologyManagerDirectiveController', [
  '$scope',
  '$state',
  '$modal',
  '$controller',
  'WorkersCompService',
  function($scope,
           $state,
           $modal,
           $controller,
           WorkersCompService){

    // Inherite scope from base
    $controller('modalMessageControllerBase', {$scope: $scope});

    // The view needs both employee and company information to generate
    // right context information for operations
    $scope.$watchGroup(['employeePersonId', 'companyId'], function(newValues) {
        var employeePersonId = newValues[0];
        var companyId = newValues[1];
        if(employeePersonId && companyId){
            WorkersCompService.GetActiveEmployeePhraseology(employeePersonId).then(function(activePhraseology) {
                $scope.employeePhraseology = activePhraseology;
                var phraseologyToEnsure = $scope.employeePhraseology
                                         ? $scope.employeePhraseology.phraseology
                                         : null;
                WorkersCompService.GetCompanyPhraseologiesWithPredefinedPhraseology(companyId, phraseologyToEnsure)
                    .then(function(companyPhraseologies) {
                        $scope.companyPhraseologies = companyPhraseologies;

                        refreshPhraseologyInfoForDisplay();
                    });
            });
        }
    });

    // Refresh the phraseology information for display
    // based on the current data in scope context.
    var refreshPhraseologyInfoForDisplay = function() {
        $scope.phraseologyInfo = getPhraseologyInfoForDisplay(
                        $scope.companyPhraseologies,
                        $scope.employeePhraseology
                    );
    };

    // Extract data from the employee phraseology and company phraseologies data
    // to compose a view model that is friendly for display
    var getPhraseologyInfoForDisplay = function(companyPhraseologies, employeePhraseology) {
        var result = {
            description: 'N/A',
            phraseology: 'N/A'
        };

        if (employeePhraseology && companyPhraseologies) {
            var employeeCompanyPhraseology = _.find(companyPhraseologies, function(phraseology) {
                                                return phraseology.phraseology.id == employeePhraseology.phraseology.id;
                                            });
            if (employeeCompanyPhraseology) {
                result.description = employeeCompanyPhraseology.description;
                result.phraseology = employeeCompanyPhraseology.phraseology.phraseology;
            }
        }

        return result;
    };

    $scope.openEditModal = function() {
        var modalInstance = $modal.open({
            templateUrl: '/static/partials/workers_comp/modal_edit_employee_phraseology.html',
            controller: 'EmployeePhraseologyModalController',
            backdrop: 'static',
            size: 'md',
            resolve: {
                companyPhraseologies: function() {
                    return $scope.companyPhraseologies;
                },
                employeePersonId: function() {
                    return $scope.employeePersonId;
                },
                employeePhraseology: function() {
                    return angular.copy($scope.employeePhraseology);
                }
            }
        });

        modalInstance.result.then(function(resultEmployeePhraseology){
            if (resultEmployeePhraseology){
              var successMessage = "Your change has been successfully saved.";
              $scope.showMessageWithOkayOnly('Success', successMessage);

              $scope.employeePhraseology = resultEmployeePhraseology;
              refreshPhraseologyInfoForDisplay();
            } else{
              var message = 'Failed to save the changes. Please try again later.';
              $scope.showMessageWithOkayOnly('Error', message);
            }
        });
    };
  }
]).directive('bmEmployeePhraseologyManager', function(){

    return {
        restrict: 'E',
        scope: {
            companyId: '=',
            employeePersonId: '='
        },
        templateUrl: '/static/partials/workers_comp/directive_employee_phraseology_manager.html',
        controller: 'EmployeePhraseologyManagerDirectiveController'
      };
});
