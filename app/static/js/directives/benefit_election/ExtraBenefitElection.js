BenefitMyApp.directive('bmExtraBenefitElection', function() {

  var controller = [
    '$scope',
    '$location',
    '$window',
    '$attrs',
    '$modal',
    'UserService',
    'ExtraBenefitService',
    function ExtraBenefitElectionDirectiveController(
      $scope,
      $location,
      $window,
      $attrs,
      $modal,
      UserService,
      ExtraBenefitService) {

        UserService.getCurUserInfo()
        .then(function(userInfo){
            ExtraBenefitService.getPersonPlanByUser(userInfo.user.id, userInfo.currentRole.company.id, true)
            .then(function(personPlan) {
                $scope.personPlan = personPlan;
            });
        });

        $scope.showSaveSuccessModal = function() {
            var modalInstance = $modal.open({
                templateUrl: '/static/partials/benefit_selection/modal_save_success.html',
                controller: function($scope) {
                                $scope.ok = function () {
                                  modalInstance.close();
                                };
                            },
                size: 'sm',
                backdrop: 'static'
            });

            return modalInstance;
        };

        $scope.save = function() {
            // Save plan selection
            ExtraBenefitService.savePersonPlan($scope.personPlan)
            .then(
                function() {
                    $scope.myForm.$setPristine();

                    var modalInstance = $scope.showSaveSuccessModal();
                    modalInstance.result.then(function(){
                        if ($scope.onSaveSuccess) {
                            $scope.onSaveSuccess();
                        }
                    });
                }
              , function(error) {
                    alert('Failed to save your benefits election. Please try again later.');
                }
            );
        };
    }
  ];

  return {
    restrict: 'E',
    scope: {
        onSaveSuccess: '&'
    },
    templateUrl: '/static/partials/benefit_selection/directive_extra_benefit.html',
    controller: controller
  };
});
