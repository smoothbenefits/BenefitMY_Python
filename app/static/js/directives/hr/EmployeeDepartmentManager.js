BenefitMyApp.controller('EmployeeDepartmentModalController', [
  '$scope',
  '$modalInstance', 
  'WorkersCompService',
  'companyDepartments',
  'employeePersonId',
  'employeePhraseology', 
  function($scope, 
           $modalInstance,
           WorkersCompService,
           companyDepartments,
           employeePersonId,
           employeePhraseology){

    $scope.modalHeader = 'Change Employee Department Assignment';

    // Set the model object in focus
    // For now, we only allow reassignment. i.e. create new
    // records and not update existing ones
    $scope.contextEmployeePhraseology = WorkersCompService.GetBlankEmployeePhraseologyByEmployeePerson(employeePersonId);

    $scope.companyDepartments = companyDepartments;

    if (employeePhraseology) {
        // Find the phraseology from the company departments dropdown
        // This is the workaround to get the dropdown selection
        // properly initialized. Due to Angular not working properly
        // when select as and track by used together.
        var currentDepartment = _.find($scope.companyDepartments, function(department) {
            return department.phraseology.id == employeePhraseology.phraseology.id;
        });
        
        $scope.contextEmployeePhraseology.phraseology = currentDepartment.phraseology;
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
]).controller('EmployeeDepartmentManagerDirectiveController', [
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
                WorkersCompService.GetCompanyDepartmentsIncludePhraseology(companyId, phraseologyToEnsure).then(function(companyDepartments) {
                    $scope.companyDepartments = companyDepartments;
                    
                    refreshDepartmentInfoForDisplay();
                });
            });
        }
    });

    // Refresh the department information for display
    // based on the current data in scope context.
    var refreshDepartmentInfoForDisplay = function() {
        $scope.departmentInfo = getDepartmentInfoForDisplay(
                        $scope.companyDepartments,
                        $scope.employeePhraseology
                    );
    };

    // Extract data from the employee phraseology and company departments data
    // to compose a view model that is friendly for display
    var getDepartmentInfoForDisplay = function(companyDepartments, employeePhraseology) {
        var result = {
            description: 'N/A',
            phraseology: 'N/A'
        };

        if (employeePhraseology && companyDepartments) {
            var employeeCompanyDepartment = _.find(companyDepartments, function(department) {
                                                return department.phraseology.id == employeePhraseology.phraseology.id;
                                            });
            if (employeeCompanyDepartment) {
                result.description = employeeCompanyDepartment.description;
                result.phraseology = employeeCompanyDepartment.phraseology.phraseology;
            }
        }

        return result;
    };

    $scope.openEditModal = function() {
        var modalInstance = $modal.open({
            templateUrl: '/static/partials/workers_comp/modal_edit_employee_department.html',
            controller: 'EmployeeDepartmentModalController',
            backdrop: 'static',
            size: 'md',
            resolve: {
                companyDepartments: function() {
                    return $scope.companyDepartments;
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
              var successMessage = "Your change to the department has been successfully saved.";
              $scope.showMessageWithOkayOnly('Success', successMessage);

              $scope.employeePhraseology = resultEmployeePhraseology;
              refreshDepartmentInfoForDisplay();
            } else{
              var message = 'Failed to save the changes. Please try again later.';
              $scope.showMessageWithOkayOnly('Error', message);
            }
        });
    };
  }
]).directive('bmEmployeeDepartmentManager', function(){

    return {
        restrict: 'E',
        scope: {
            companyId: '=',
            employeePersonId: '='
        },
        templateUrl: '/static/partials/workers_comp/directive_employee_department_manager.html',
        controller: 'EmployeeDepartmentManagerDirectiveController'
      };
});