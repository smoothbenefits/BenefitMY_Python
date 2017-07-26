BenefitMyApp.controller('JobModalController', [
  '$scope',
  '$modalInstance',
  'CompanyJobService',
  'companyId',
  'job',
  function($scope,
           $modalInstance,
           CompanyJobService,
           companyId,
           job){

    // When a model is passed in, it means we are in
    // edit (vs creation) mode
    $scope.editMode = job;

    $scope.modalHeader = $scope.editMode
        ? 'Edit Job Info'
        : 'Create a New Job';

    // Set the model object in focus
    // If in edit mode, use the model passed in.
    // Else use a blank model created from the service
    $scope.contextJob = $scope.editMode
        ? job
        : CompanyJobService.GetBlankCompanyJobByCompanyId(companyId);

    $scope.cancel = function() {
        $modalInstance.dismiss();
    };

    $scope.save = function() {
        CompanyJobService.SaveCompanyJob($scope.contextJob).then(
            function(resultJob) {
                $modalInstance.close(resultJob);
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
            && $scope.contextJob.job;
    };
  }
]).controller('JobManagerDirectiveController', [
  '$scope',
  '$state',
  '$modal',
  '$controller',
  'CompanyJobService',
  function($scope,
           $state,
           $modal,
           $controller,
           CompanyJobService){

    // Inherite scope from base
    $controller('modalMessageControllerBase', {$scope: $scope});

    $scope.$watch('companyId', function(companyId) {
        if(companyId){
            CompanyJobService.GetCompanyJobs(companyId)
            .then(function(companyJobs) {
                $scope.companyJobs = companyJobs;
            });
        }
    });

    $scope.hasJobs = function() {
      return $scope.companyJobs && $scope.companyJobs.length > 0;
    };

    $scope.openEditModal = function(job) {
        var modalInstance = $modal.open({
            templateUrl: '/static/partials/company_info/modal_edit_job.html',
            controller: 'JobModalController',
            backdrop: 'static',
            size: 'md',
            resolve: {
                companyId: function() {
                    return $scope.companyId;
                },
                job: function() {
                    return angular.copy(job);
                }
            }
        });

        modalInstance.result.then(function(resultJob){
            if (resultJob){
              var successMessage = "Your change has been successfully saved.";

              $scope.showMessageWithOkayOnly('Success', successMessage);
            } else{
              var message = 'Failed to save the changes. Please try again later.';
              $scope.showMessageWithOkayOnly('Error', message);
            }

            $state.reload();
        });
    };

    $scope.deleteConfirmMsg = 'Are you sure you want to delete this job setup?';

    $scope.deleteJob = function(job) {
        CompanyJobService.DeleteCompanyJob(job)
        .then(function(response) {
            $state.reload();
        });
    };
  }
]).directive('bmJobManager', function(){

    return {
        restrict: 'E',
        scope: {
            companyId: '='
        },
        templateUrl: '/static/partials/company_info/directive_job_manager.html',
        controller: 'JobManagerDirectiveController'
      };
});
