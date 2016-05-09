BenefitMyApp.controller('DepartmentModalController', [
  '$scope',
  '$modalInstance', 
  'WorkersCompService',
  'company',
  'department', 
  function($scope, 
           $modalInstance,
           WorkersCompService,
           company,
           department){
    WorkersCompService.GetAllPhraseologys().then(function(allPhraseologys) {
        $scope.allPhraseologys = allPhraseologys;
    });

    // Perform search based on text term. 
    // This is to support filtering on typeahead
    $scope.searchPhraseologys = function(term){
        var lowerTerm = term.toLowerCase();
        return _.filter($scope.allPhraseologys, function(entry){
          return entry.phraseology.toLowerCase().indexOf(lowerTerm) > -1;
        });
    };

    // When a model is passed in, it means we are in
    // edit (vs creation) mode
    $scope.editMode = department;

    $scope.modalHeader = $scope.editMode ? 'Edit Department Info' : 'Create a New Department';

    // Set the model object in focus
    // If in edit mode, use the model passed in.
    // Else use a blank model created from the service
    $scope.contextDepartment = $scope.editMode 
        ? department
        : WorkersCompService.GetBlankCompanyDepartmentByCompany(company);

    $scope.cancel = function() {
        $modalInstance.dismiss();
    };

    $scope.save = function() {
        WorkersCompService.SaveCompanyPhraseology($scope.contextDepartment).then(
            function(resultDepartment) {
                $modalInstance.close(resultDepartment);
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
            && $scope.contextDepartment.phraseology
            && $scope.contextDepartment.phraseology.id;
    };
  }
]).controller('DepartmentManagerDirectiveController', [
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

    $scope.$watch('company', function(company) {
        if(company){
            WorkersCompService.GetCompanyDepartments(company.id).then(function(companyDepartments) {
                $scope.companyDepartments = companyDepartments;
            });
        }
    });

    $scope.openEditModal = function(department) {
        var modalInstance = $modal.open({
            templateUrl: '/static/partials/workers_comp/modal_edit_department.html',
            controller: 'DepartmentModalController',
            backdrop: 'static',
            size: 'md',
            resolve: {
                company: function() {
                    return $scope.company;
                },
                department: function() {
                    return angular.copy(department);
                }
            }
        });

        modalInstance.result.then(function(resultDepartment){
            if (resultDepartment){
              var successMessage = "Your change to the department has been successfully saved.";

              $scope.showMessageWithOkayOnly('Success', successMessage);
            } else{
              var message = 'Failed to save the changes. Please try again later.';
              $scope.showMessageWithOkayOnly('Error', message);
            }

            $state.reload();
        });
    };

    $scope.deleteConfirmMsg = 'Are you sure you want to delete this department setup?';
  
    $scope.deleteDepartment = function(department) {
        WorkersCompService.DeleteCompanyPhraseology(department)
        .then(function(response) {
            $state.reload();
        });
    };
  }
]).directive('bmDepartmentManager', function(){

    return {
        restrict: 'E',
        scope: {
            company: '='
        },
        templateUrl: '/static/partials/workers_comp/directive_department_manager.html',
        controller: 'DepartmentManagerDirectiveController'
      };
});