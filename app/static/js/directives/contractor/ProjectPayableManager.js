BenefitMyApp.controller('ProjectPayableModalController', [
  '$scope',
  '$modalInstance',
  'ProjectService',
  'ContractorsService',
  'payable',
  'projectId',
  'contractors',
  function(
    $scope,
    $modalInstance,
    ProjectService,
    ContractorsService,
    payable,
    projectId,
    contractors) {

    $scope.editMode = payable;

    $scope.modalHeader = $scope.editMode ? 'Edit Payable Info' : 'Create a New Payable';

    $scope.contractors = contractors;

    $scope.payable = $scope.editMode
                        ? payable
                        : ProjectService.GetBlankProjectPayable(projectId);

    if ($scope.editMode) {
      $scope.payable.contractor = _.find(contractors, function(contractor) {
        return contractor._id === $scope.payable.contractor._id;
      });
    }

    $scope.enableSave = function(payable) {
      if (moment(payable.dateStart).isAfter(moment(payable.dateEnd))) {
        return false;
      }

      if (!payable.amount || payable.amount <= 0) {
        return false;
      }

      return payable.contractor;
    };

    $scope.cancel = function() {
      $modalInstance.dismiss();
    };

    $scope.save = function() {
      ProjectService.SaveProjectPayable(projectId, $scope.payable)
        .then(function(savedPayable){
          $modalInstance.close(true);
        }, function(error){
          $modalInstance.close(false)
        });
    }
  }
]).controller('ProjectPayableManagerDirectiveController', [
  '$scope',
  '$state',
  '$modal',
  '$controller',
  'ProjectService',
  'ContractorsService',
  'utilityService',
  function($scope,
           $state,
           $modal,
           $controller,
           ProjectService,
           ContractorsService,
           utilityService){

    // Inherite scope from base
    $controller('modalMessageControllerBase', {$scope: $scope});

    $scope.$watch('project', function(project) {
        if(project){
          var companyId = utilityService.retrieveIdFromEnvAwareId(project.companyDescriptor);

          ContractorsService.GetContractorsByCompany(companyId).then(function(contractors) {
            $scope.contractors = contractors;
          });
        }
    });

    $scope.openPayableModal = function(payable) {
      var modalInstance = $modal.open({
        templateUrl: '/static/partials/contractor/modal_project_payable.html',
        controller: 'ProjectPayableModalController',
        backdrop: 'static',
        size: 'lg',
        resolve: {
          payable: function() {
            return angular.copy(payable);
          },
          projectId: function() {
            return $scope.project._id;
          },
          contractors: function() {
            return angular.copy($scope.contractors);
          }
        }
      });

      modalInstance.result.then(function(success){
        if(success){
          var successMessage = "Project Payable saved successfully!";
          $scope.showMessageWithOkayOnly('Success', successMessage);
        }
        else{
          var message = "Project Payable save failed!";
          $scope.showMessageWithOkayOnly('Error', message);
        }
        $state.reload();
      });
    };

    $scope.hasPayablesMade = function() {
        return $scope.project
            && $scope.project.payables
            && $scope.project.payables.length > 0;
    };

    $scope.delete = function(payable) {
      ProjectService.DeletePayableByProjectPayable($scope.project._id, payable)
      .then(function(res){
        $state.reload();
      });
    };
  }
]).directive('bmProjectPayableManager', function(){

    return {
        restrict: 'E',
        scope: {
            project: '='
        },
        templateUrl: '/static/partials/contractor/directive_project_payable_manager.html',
        controller: 'ProjectPayableManagerDirectiveController'
      };
});
