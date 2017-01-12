BenefitMyApp.controller('PhraseologyModalController', [
  '$scope',
  '$modalInstance',
  'WorkersCompService',
  'company',
  'phraseology',
  function($scope,
           $modalInstance,
           WorkersCompService,
           company,
           phraseology){
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
    $scope.editMode = phraseology;

    $scope.modalHeader = $scope.editMode
        ? 'Edit Worker''s Comp Department (Phraseology) Info'
        : 'Create a New Worker''s Comp Department (Phraseology)';

    // Set the model object in focus
    // If in edit mode, use the model passed in.
    // Else use a blank model created from the service
    $scope.contextPhraseology = $scope.editMode
        ? phraseology
        : WorkersCompService.GetBlankCompanyPhraseologyByCompany(company);

    $scope.cancel = function() {
        $modalInstance.dismiss();
    };

    $scope.save = function() {
        WorkersCompService.SaveCompanyPhraseology($scope.contextPhraseology).then(
            function(resultPhraseology) {
                $modalInstance.close(resultPhraseology);
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
            && $scope.contextPhraseology.phraseology
            && $scope.contextPhraseology.phraseology.id;
    };
  }
]).controller('PhraseologyManagerDirectiveController', [
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
            WorkersCompService.GetCompanyPhraseologies(company.id).then(function(companyPhraseologies) {
                $scope.companyPhraseologies = companyPhraseologies;
            });
        }
    });

    $scope.openEditModal = function(phraseology) {
        var modalInstance = $modal.open({
            templateUrl: '/static/partials/workers_comp/modal_edit_phraseology.html',
            controller: 'PhraseologyModalController',
            backdrop: 'static',
            size: 'md',
            resolve: {
                company: function() {
                    return $scope.company;
                },
                phraseology: function() {
                    return angular.copy(phraseology);
                }
            }
        });

        modalInstance.result.then(function(resultPhraseology){
            if (resultPhraseology){
              var successMessage = "Your change has been successfully saved.";

              $scope.showMessageWithOkayOnly('Success', successMessage);
            } else{
              var message = 'Failed to save the changes. Please try again later.';
              $scope.showMessageWithOkayOnly('Error', message);
            }

            $state.reload();
        });
    };

    $scope.deleteConfirmMsg = 'Are you sure you want to delete this phraseology setup?';

    $scope.deletePhraseology = function(phraseology) {
        WorkersCompService.DeleteCompanyPhraseology(phraseology)
        .then(function(response) {
            $state.reload();
        });
    };
  }
]).directive('bmPhraseologyManager', function(){

    return {
        restrict: 'E',
        scope: {
            company: '='
        },
        templateUrl: '/static/partials/workers_comp/directive_phraseology_manager.html',
        controller: 'PhraseologyManagerDirectiveController'
      };
});
