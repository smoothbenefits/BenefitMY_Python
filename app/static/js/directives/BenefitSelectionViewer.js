BenefitMyApp.directive('bmBenefitSelectionViewer', function() {

  var controller = [
    '$scope',
    '$location',
    '$window',
    '$attrs',
    '$controller',
    'FsaService',
    'BasicLifeInsuranceService',
    'SupplementalLifeInsuranceService',
    'StdService',
    'LtdService',
    'HraService',
    'CommuterService',
    function CompanyInfoEditorDirectiveController(
      $scope,
      $location,
      $window,
      $attrs,
      $controller,
      FsaService,
      BasicLifeInsuranceService,
      SupplementalLifeInsuranceService,
      StdService,
      LtdService,
      HraService,
      CommuterService) {

      $controller('userController', {$scope: $scope});

      $scope.$watch('user', function(theUser) {
          if(theUser){
              // FSA election data
              FsaService.getFsaElectionForUser($scope.user.id, $scope.company.id).then(function(fsaPlan){
                $scope.fsaElection = fsaPlan;
              });

              // Supplemental Life Insurance
              SupplementalLifeInsuranceService.getPlanByUser($scope.user.id, $scope.company).then(function(plan) {
                $scope.supplementalLifeInsurancePlan = plan;
              });

              // Basic Life Insurance
              BasicLifeInsuranceService.getBasicLifeInsuranceEnrollmentByUser($scope.user.id, $scope.company)
              .then(function(response){
                $scope.basicLifeInsurancePlan = response;
              });

              // STD
              StdService.getUserEnrolledStdPlanByUser($scope.user.id).then(function(response){
                $scope.userStdPlan = response;
              });

              // LTD
              LtdService.getUserEnrolledLtdPlanByUser($scope.user.id, $scope.company.id).then(function(response){
                $scope.userLtdPlan = response;
              });

              // HRA
              HraService.getPersonPlanByUser($scope.user.id, $scope.company.id).then(function(response){
                $scope.hraPlan = response;
              });

              // Commuter
              CommuterService.getPersonPlanByUser($scope.user.id).then(function(response){
                if(response){
                  $scope.commuterPlan = response;
                  $scope.commuterPlan.calculatedTotalTransitAllowance = CommuterService.computeTotalMonthlyTransitAllowance($scope.commuterPlan);
                  $scope.commuterPlan.calculatedTotalParkingAllowance = CommuterService.computeTotalMonthlyParkingAllowance($scope.commuterPlan);
                }
              });
          }
      });

    }
  ];

  return {
    restrict: 'E',
    scope: {
        user: '=',
        company: '='
    },
    templateUrl: '/static/partials/benefit_view/directive_benefit_selection_viewer.html',
    controller: controller
  };
});
