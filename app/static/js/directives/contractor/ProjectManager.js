BenefitMyApp.controller('ProjectModalController', [
  '$scope', '$modalInstance', 'project',
  function($scope, $modalInstance, project){
    $scope.companyContractors =[
        { name: 'Burlington HVAC' },
        { name: 'Woburn Plumbing'},
        { name: 'Lexington Flooring' }
    ];

    $scope.insuranceTypes = [
        { name: 'Commercial General Liability' },
        { name: 'Umbrella Liability' },
        { name: 'Excess Liability' },
        { name: 'Worker\'s Compensation and Employee Liability' }
    ];

    $scope.editMode = project;

    $scope.modalHeader = $scope.editMode ? 'Edit Project Info' : 'Create a New Project';

    $scope.contextProject = $scope.editMode ? project : {};

    $scope.isProjectActive = function() {
        return $scope.contextProject.status == 'Active';
    };

    $scope.toggleActivate = function() {
        $scope.contextProject.status = $scope.isProjectActive()
                                        ? 'Inactive'
                                        : 'Active';
    };

    $scope.cancel = function() {
        $modalInstance.dismiss();
    };

    $scope.save = function() {
        $modalInstance.close(true);
    }
  }
]).controller('ProjectManagerDirectiveController', [
  '$scope',
  '$state',
  '$modal',
  '$controller',
  function($scope,
           $state,
           $modal,
           $controller){

    // Inherite scope from base
    $controller('modalMessageControllerBase', {$scope: $scope});

    $scope.activeProjects = [
        {
            name: 'AMC at Woburn',
            address: '39 Aloha Street, Woburn, MA',
            contractors: [
                { name: 'Burlington HVAC' },
                { name: 'Lexington Flooring' }
            ],
            requiredInsuranceTypes: [
                'Commercial General Liability',
                'Umbrella Liability',
            ],
            status: 'Active'
        },
        {
            name: 'Lexington Music School',
            address: '44 Main Street, Lexington, MA',
            contractors: [
                { name: 'Woburn Plumbing' },
                { name: 'Lexington Flooring' }
            ],
            requiredInsuranceTypes: [
                'Umbrella Liability',
                'Excess Liability',
                'Worker\'s Compensation and Employee Liability'
            ],
            status: 'Active'
        }
    ];

    $scope.inactiveProjects = [
        {
            name: 'Newton High Gym',
            address: '92 Pleasant Road, Newton, MA',
            contractors: [
                { name: 'Lexington Flooring' }
            ],
            requiredInsuranceTypes: [
                'Umbrella Liability',
                'Worker\'s Compensation and Employee Liability'
            ],
            status: 'Inactive'
        }
    ];

    $scope.openProjectModal = function(project) {
        $modal.open({
            templateUrl: '/static/partials/contractor/modal_project.html',
            controller: 'ProjectModalController',
            backdrop: 'static',
            size: 'md',
            resolve: {
                project: function() {
                  return angular.copy(project);
                },
            }
        });
    }
  }
]).directive('bmProjectManager', function(){

    return {
        restrict: 'E',
        scope: {
        },
        templateUrl: '/static/partials/contractor/directive_project_manager.html',
        controller: 'ProjectManagerDirectiveController'
      };
});
