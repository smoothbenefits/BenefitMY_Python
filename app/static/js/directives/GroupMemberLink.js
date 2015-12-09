BenefitMyApp.controller('CompanyGroupMemberUpdateModalController', [
  '$scope', '$modalInstance', 'CompanyBenefitGroupService', 'groupMember', 'companyId',
  function($scope, $modalInstance, CompanyBenefitGroupService, groupMember, companyId) {
    $scope.groupMember = groupMember;
    CompanyBenefitGroupService.GetCompanyBenefitGroupByCompany(companyId)
    .then(function(groups){
      $scope.groups = groups;
    });

    $scope.save = function() {
      if($scope.groupMember.id){
        CompanyBenefitGroupService.UpdateCompanyGroupMembership($scope.groupMember)
        .then(function(response) {
          $modalInstance.close(response);
        });
      }
      else{
        //We should just assign this employee to the selected group
        CompanyBenefitGroupService.AddNewCompanyGroupMembership($scope.groupMember.user, $scope.groupMember.company_group)
        .then(function(response){
          $modalInstance.close(response);
        });
      }
    };

    $scope.cancel = function() {
      $modalInstance.dismiss();
    };
  }
]).directive('bmGroupMemberLink', function() {
  var memberLinkController = [
    '$scope', '$modal',
    function BenefitGroupManagerDirectiveController(
      $scope, $modal) {
        $scope.showEditMemberModal = function(){
          var modalInstance = $modal.open({
            templateUrl: '/static/partials/common/modal_update_group_member.html',
            controller: 'CompanyGroupMemberUpdateModalController',
            size: 'md',
            resolve: {
              groupMember: function(){
                var gm = {
                  id: $scope.groupMember.id,
                  company_group: $scope.groupMember.company_group.id,
                  user: $scope.user
                };
                return gm;
              },
              companyId: function(){
                return $scope.companyId;
              }
            }
          });
          modalInstance.result.then(function(newGroupMember){
            $scope.groupMember = newGroupMember;
          });
        };
    }];
return {
      restrict: 'E',
      template:'<a ng-click="showEditMemberModal()" href="javascript:void(0);">{{groupMember.company_group.name}}</a>',
      controller: memberLinkController,
      scope: {
        groupMember: '=',
        user: '=',
        companyId: '='
      },
    }
  }
);