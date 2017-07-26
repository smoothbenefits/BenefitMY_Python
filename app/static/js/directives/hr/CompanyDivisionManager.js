BenefitMyApp.controller('DivisionModalController', [
  '$scope',
  '$modalInstance',
  'CompanyDivisionService',
  'companyId',
  'division',
  function($scope,
           $modalInstance,
           CompanyDivisionService,
           companyId,
           division){

    // When a model is passed in, it means we are in
    // edit (vs creation) mode
    $scope.editMode = division;

    $scope.modalHeader = $scope.editMode
        ? 'Edit Division Info'
        : 'Create a New Division';

    // Set the model object in focus
    // If in edit mode, use the model passed in.
    // Else use a blank model created from the service
    $scope.contextDivision = $scope.editMode
        ? division
        : CompanyDivisionService.GetBlankCompanyDivisionByCompanyId(companyId);

    $scope.cancel = function() {
        $modalInstance.dismiss();
    };

    $scope.save = function() {
        CompanyDivisionService.SaveCompanyDivision($scope.contextDivision).then(
            function(resultDivision) {
                $modalInstance.close(resultDivision);
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
            && $scope.contextDivision.division;
    };
  }
]).controller('DivisionManagerDirectiveController', [
  '$scope',
  '$state',
  '$modal',
  '$controller',
  'CompanyDivisionService',
  function($scope,
           $state,
           $modal,
           $controller,
           CompanyDivisionService){

    // Inherite scope from base
    $controller('modalMessageControllerBase', {$scope: $scope});

    $scope.$watch('companyId', function(companyId) {
        if(companyId){
            CompanyDivisionService.GetCompanyDivisions(companyId)
            .then(function(companyDivisions) {
                $scope.companyDivisions = companyDivisions;
            });
        }
    });

    $scope.hasDivisions = function() {
      return $scope.companyDivisions && $scope.companyDivisions.length > 0;
    };

    $scope.openEditModal = function(division) {
        var modalInstance = $modal.open({
            templateUrl: '/static/partials/company_info/modal_edit_division.html',
            controller: 'DivisionModalController',
            backdrop: 'static',
            size: 'md',
            resolve: {
                companyId: function() {
                    return $scope.companyId;
                },
                division: function() {
                    return angular.copy(division);
                }
            }
        });

        modalInstance.result.then(function(resultDivision){
            if (resultDivision){
              var successMessage = "Your change has been successfully saved.";

              $scope.showMessageWithOkayOnly('Success', successMessage);
            } else{
              var message = 'Failed to save the changes. Please try again later.';
              $scope.showMessageWithOkayOnly('Error', message);
            }

            $state.reload();
        });
    };

    $scope.deleteConfirmMsg = 'Are you sure you want to delete this division setup?';

    $scope.deleteDivision = function(division) {
        CompanyDivisionService.DeleteCompanyDivision(division)
        .then(function(response) {
            $state.reload();
        });
    };
  }
]).directive('bmDivisionManager', function(){

    return {
        restrict: 'E',
        scope: {
            companyId: '='
        },
        templateUrl: '/static/partials/company_info/directive_division_manager.html',
        controller: 'DivisionManagerDirectiveController'
      };
});
