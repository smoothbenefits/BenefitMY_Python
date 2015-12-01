BenefitMyApp.directive('bmBenefitGroupManager', function() {

  var controller = [
    '$scope',
    '$state',
    function BenefitGroupManagerDirectiveController(
      $scope, $state) {

      }
    )
  ];

  return {
    restrict: 'E',
    scope: {
      target: '=',
      editorUserId: '=?'
    },
    templateUrl: '/static/partials/common/directive_benefit_group_manager.html',
    controller: controller
  };
});
