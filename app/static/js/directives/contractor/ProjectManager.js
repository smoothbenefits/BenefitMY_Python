BenefitMyApp.controller('ProjectModalController', [
  '$scope',
  '$modalInstance',
  'ProjectService',
  'ContractorsService',
  'project',
  'companyId',
  function(
    $scope,
    $modalInstance,
    ProjectService,
    ContractorsService,
    project,
    companyId) {

    $scope.insuranceTypes = ContractorsService.InsuranceCertificateTypes;

    $scope.editMode = project;

    $scope.modalHeader = $scope.editMode ? 'Edit Project Info' : 'Create a New Project';

    $scope.contextProject = $scope.editMode
                        ? project
                        : ProjectService.GetBlankProject(companyId);

    var convertInsuranceTypeListForSelection = function(insuranceTypeList) {
        return _.map(insuranceTypeList, function(type) {
            return { name: type };
        });
    };

    var convertInsuranceTypeSelectionsToList = function(selectionList) {
        return _.map(selectionList, function(selectionItem) {
            return selectionItem.name;
        });
    };

    $scope.insuranceTypesForSelection = convertInsuranceTypeListForSelection($scope.insuranceTypes);
    $scope.insuranceTypesSelected = convertInsuranceTypeListForSelection($scope.contextProject.requiredInsuranceTypes);

    _.each($scope.insuranceTypesForSelection, function(item) {
        if (_.some($scope.insuranceTypesSelected, function(selected) {
                return selected.name == item.name;
        })) {
            item.ticked = true;
        }
    });

    $scope.inputInvalid = function(){
      return !$scope.contextProject ||
        !$scope.contextProject.name ||
        !$scope.insuranceTypesSelected ||
        $scope.insuranceTypesSelected.length == 0;
    };

    $scope.cancel = function() {
        $modalInstance.dismiss();
    };

    $scope.save = function() {
        $scope.contextProject.requiredInsuranceTypes = convertInsuranceTypeSelectionsToList($scope.insuranceTypesSelected);
        ProjectService.SaveProject($scope.contextProject)
          .then(function(savedProject){
            $modalInstance.close(true);
          }, function(error){
            $modalInstance.close(false)
          });
    }
  }
]).controller('ProjectManagerDirectiveController', [
  '$scope',
  '$state',
  '$modal',
  '$controller',
  'ProjectService',
  'utilityService',
  function($scope,
           $state,
           $modal,
           $controller,
           ProjectService,
           utilityService){

    // Inherite scope from base
    $controller('modalMessageControllerBase', {$scope: $scope});

    $scope.$watch('company', function(company) {
        if(company){
            ProjectService.GetProjectsByCompany(company.id)
            .then(function(projects){
                var projectsByStatus = _.groupBy(projects, 'status');
                $scope.activeProjects = projectsByStatus[ProjectService.ProjectStatus.Active];
                $scope.inactiveProjects = projectsByStatus[ProjectService.ProjectStatus.Inactive];
            });
        }
    });

    $scope.getAddressForDisplay = utilityService.getAddressForDisplay;

    $scope.openProjectModal = function(project) {
        var modalInstance = $modal.open({
            templateUrl: '/static/partials/contractor/modal_project.html',
            controller: 'ProjectModalController',
            backdrop: 'static',
            size: 'lg',
            resolve: {
                project: function() {
                  return angular.copy(project);
                },
                companyId: function() {
                    return $scope.company.id;
                }
            }
        });

        modalInstance.result.then(function(success){
          if(success){
            var successMessage = "Project saved successfully!";
            $scope.showMessageWithOkayOnly('Success', successMessage);
          }
          else{
            var message = "Project save failed!";
            $scope.showMessageWithOkayOnly('Error', message);
          }
          $state.reload();
        });
    };

    $scope.hasInactiveProjects = function() {
        return $scope.inactiveProjects
            && $scope.inactiveProjects.length > 0;
    };

    $scope.hasActiveProjects = function() {
        return $scope.activeProjects
            && $scope.activeProjects.length > 0;
    };

    $scope.activate = function(project) {
        ProjectService.SetProjectStatus(project, ProjectService.ProjectStatus.Active)
        .then(function(updatedProject){
          $state.reload();
        });
    };

    $scope.deactivate = function(project) {
        ProjectService.SetProjectStatus(project, ProjectService.ProjectStatus.Inactive)
        .then(function(updatedProject){
          $state.reload();
        });
    };

    $scope.managePayables = function(project) {
      $state.go('admin_project_payable', {projectId: project._id});
    };
  }
]).directive('bmProjectManager', function(){

    return {
        restrict: 'E',
        scope: {
            company: '='
        },
        templateUrl: '/static/partials/contractor/directive_project_manager.html',
        controller: 'ProjectManagerDirectiveController'
      };
});
