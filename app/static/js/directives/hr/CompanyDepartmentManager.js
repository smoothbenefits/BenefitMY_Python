BenefitMyApp.controller('DepartmentModalController', [
  '$scope',
  '$modalInstance',
  'CompanyDepartmentService',
  'company',
  'department',
  function($scope,
           $modalInstance,
           CompanyDepartmentService,
           company,
           department){

    // When a model is passed in, it means we are in
    // edit (vs creation) mode
    $scope.editMode = department;

    $scope.modalHeader = $scope.editMode
        ? 'Edit Department Info'
        : 'Create a New Department';

    // Set the model object in focus
    // If in edit mode, use the model passed in.
    // Else use a blank model created from the service
    $scope.contextDepartment = $scope.editMode
        ? phraseology
        : CompanyDepartmentService.GetBlankCompanyDepartmentByCompany(company);

    $scope.cancel = function() {
        $modalInstance.dismiss();
    };

    $scope.save = function() {
        CompanyDepartmentService.SaveCompanyDepartment($scope.contextDepartment).then(
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
            && $scope.contextDepartment.department;
    };
  }
]).controller('DepartmentManagerDirectiveController', [
  '$scope',
  '$state',
  '$modal',
  '$controller',
  'CompanyDepartmentService',
  function($scope,
           $state,
           $modal,
           $controller,
           CompanyDepartmentService){

    // Inherite scope from base
    $controller('modalMessageControllerBase', {$scope: $scope});

    $scope.$watch('companyId', function(companyId) {
        if(companyId){
            CompanyDepartmentService.GetCompanyDepartments(companyId)
            .then(function(companyDepartments) {
                $scope.companyDepartments = companyDepartments;
            });
        }
    });

    $scope.openEditModal = function(department) {
        var modalInstance = $modal.open({
            templateUrl: '/static/partials/company_info/modal_edit_department.html',
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
              var successMessage = "Your change has been successfully saved.";

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
        CompanyDepartmentService.DeleteCompanyDepartment(department)
        .then(function(response) {
            $state.reload();
        });
    };
  }
]).directive('bmDepartmentManager', function(){

    return {
        restrict: 'E',
        scope: {
            companyId: '='
        },
        templateUrl: '/static/partials/company_info/directive_department_manager.html',
        controller: 'DepartmentManagerDirectiveController'
      };
});
