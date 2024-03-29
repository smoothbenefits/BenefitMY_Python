BenefitMyApp.controller('CompanyGroupEditModalController', [
  '$scope', '$modalInstance', 'CompanyBenefitGroupService', 'companyId', 'group',
  function($scope, $modalInstance, CompanyBenefitGroupService, companyId, group) {
    $scope.group = angular.copy(group);

    $scope.save = function() {
      CompanyBenefitGroupService.UpdateCompanyGroup(companyId, $scope.group)
      .then(function(response) {
        $modalInstance.close(response);
      });
    };

    $scope.cancel = function() {
      $modalInstance.dismiss();
    };
  }
]).controller('CompanyGroupAddModalController', [
  '$scope', '$modalInstance','CompanyBenefitGroupService', 'companyId',
  function($scope, $modalInstance, CompanyBenefitGroupService, companyId) {
    $scope.save = function() {
      CompanyBenefitGroupService.AddNewCompanyGroup(companyId, $scope.group)
      .then(function(response) {
        $modalInstance.close(response);
      }, function(error) {
        $modalInstance.close(error);
      });
    };

    $scope.cancel = function() {
      $modalInstance.dismiss();
    };
  }
]).directive('bmBenefitGroupManager', function() {

  var controller = [
    '$scope', '$modal', '$state', '$controller', 'CompanyBenefitGroupService',
    function BenefitGroupManagerDirectiveController(
      $scope, $modal, $state, $controller, CompanyBenefitGroupService) {

        // Inherit base modal controller for dialog window
        $controller('modalMessageControllerBase', {$scope: $scope});

        var companyId = $scope.company;
        CompanyBenefitGroupService.GetCompanyBenefitGroupByCompany(companyId)
        .then(function(groups) {
          $scope.groups = groups;
        });

        $scope.deleteGroup = function(group) {
          CompanyBenefitGroupService.DeleteCompanyGroup(group).then(function(response) {
            $scope.showMessageWithOkayOnly('Success', group.name + ' has been deleted successfully');
            $state.reload();
          }, function(error) {
            $scope.showMessageWithOkayOnly('Error', 'Error occurred when trying to delete the group');
          });
        };

        $scope.editGroupInfo = function(group) {
          var modalInstance = $modal.open({
            templateUrl: '/static/partials/common/modal_company_group_edit.html',
            controller: 'CompanyGroupEditModalController',
            size: 'md',
            resolve: {
              companyId: function() {
                return companyId;
              },
              group: function() {
                return group;
              }
            }
          });

          modalInstance.result.then(function(group) {
            $state.reload();
          });
        };

        $scope.addNewGroup = function() {
          var modalInstance = $modal.open({
            templateUrl: '/static/partials/common/modal_company_group_edit.html',
            controller: 'CompanyGroupAddModalController',
            size: 'md',
            resolve: {
              companyId: function() {
                return companyId;
              }
            }
          });

          modalInstance.result.then(function(group) {
            $state.reload();
          });
        };
      }
  ];

  return {
    restrict: 'E',
    scope: {
      company: '='
    },
    templateUrl: '/static/partials/common/directive_benefit_group_manager.html',
    controller: controller
  };
});
