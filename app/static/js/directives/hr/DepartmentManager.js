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

    $scope.editMode = department;

    $scope.modalHeader = $scope.editMode ? 'Edit Department Info' : 'Create a New Department';

    $scope.contextDepartment = $scope.editMode 
        ? department
        : { company: company.id };

    $scope.cancel = function() {
        $modalInstance.dismiss();
    };

    $scope.save = function() {
        $modalInstance.close($scope.contextDepartment);
    }
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

            // $state.reload();

            // TODO: To remove
            if (department) {
                $scope.companyDepartments = _.reject($scope.companyDepartments, function(d) {
                    return d.id == department.id;
                });
            }

            $scope.companyDepartments.push(resultDepartment);
        });
    };

    $scope.deleteConfirmMsg = 'Are you sure you want to delete this department setup?';
  
    $scope.deleteDepartment = function(department) {
        $scope.companyDepartments = _.reject($scope.companyDepartments, function(d) {
            return d.id == department.id;
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