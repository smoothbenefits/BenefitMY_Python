BenefitMyApp.directive('bmCommuterElection', function() {

  var controller = [
    '$scope',
    '$location',
    '$window',
    '$attrs',
    '$modal',
    'UserService',
    'CommuterService',
    function CommuterElectionDirectiveController(
      $scope,
      $location,
      $window,
      $attrs,
      $modal,
      UserService,
      CommuterService) {

        UserService.getCurUserInfo()
        .then(function(userInfo){
            CommuterService.getPersonPlanByUser(userInfo.user.id, userInfo.currentRole.company.id, true)
            .then(function(personPlan) {
                $scope.personPlan = personPlan;

                var benenfitEnablementStatus = CommuterService.mapEnablementOptionToStatus($scope.personPlan.companyPlan.benefitEnablementOption);

                if (benenfitEnablementStatus) {
                    $scope.benenfitEnablementStatus = benenfitEnablementStatus;
                }
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

        $scope.openPlanDetailsModal = function() {
            var modalInstance = $modal.open({
              templateUrl: '/static/partials/benefit_selection/modal_commuter_plan_details.html',
              controller: function($scope, companyPlan) {
                                $scope.companyPlanToDisplay = companyPlan;
                                $scope.closePlanDetailsModal = function () {
                                  modalInstance.close();
                                };
                          },
              size: 'lg',
              scope: $scope,
              resolve: {
                companyPlan: function() {
                    return $scope.personPlan.companyPlan;
                }
              }
            });
        };

        $scope.save = function() {
            // Save plan selection
            CommuterService.savePersonPlan($scope.personPlan)
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

        $scope.computeTotalMonthlyParkingAllowance = function() {
            if (!$scope.personPlan) {
                return 0;
            }
            return CommuterService.computeTotalMonthlyParkingAllowance($scope.personPlan);
        };

        $scope.computeTotalMonthlyTransitAllowance = function() {
            if (!$scope.personPlan) {
                return 0;
            }
            return CommuterService.computeTotalMonthlyTransitAllowance($scope.personPlan);
        };
    }
  ];

  return {
    restrict: 'E',
    scope: {
        onSaveSuccess: '&'
    },
    templateUrl: '/static/partials/benefit_selection/directive_commuter.html',
    controller: controller
  };
});
