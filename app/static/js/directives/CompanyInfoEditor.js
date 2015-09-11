BenefitMyApp.directive('bmCompanyInfoEditor', function() {

  var controller = [
    '$scope',
    '$location',
    '$window',
    'CompanyService',
    'PeriodDefinitionRepository',
    function PersonalInfoEditorDirectiveController(
      $scope, 
      $location,
      $window, 
      CompanyService, 
      PeriodDefinitionRepository) {

        $scope.client = {};

        // CompanyService.getCompanyInfo(DUMMY_HASHED_KEY).then(function(response) {
        //     $scope.client = response;
        // });

        PeriodDefinitionRepository.query().$promise.then(function(payPeriods){
          $scope.payPeriods = payPeriods;
        });

        $scope.createClient = function(){
          CompanyService.saveCompanyInfo($scope.client).then(function(response) {
            alert('Changes saved successfully');
            $window.history.back();
          }, function(error) {
            alert("Failed to add client. " + error);
          })
        };

    }
  ];

  return {
    restrict: 'E',
    scope: {
        target: '=?'
    },
    templateUrl: '/static/partials/common/directive_company_info_edit.html',
    controller: controller
  };
});
