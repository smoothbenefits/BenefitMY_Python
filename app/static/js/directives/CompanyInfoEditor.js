BenefitMyApp.directive('bmCompanyInfoEditor', function() {

  var controller = [
    '$scope',
    '$location',
    '$window',
    '$attrs',
    'CompanyService',
    'PeriodDefinitionRepository',
    function CompanyInfoEditorDirectiveController(
      $scope,
      $location,
      $window,
      $attrs,
      CompanyService,
      PeriodDefinitionRepository) {

        $scope.client = {};

        if ($scope.target) {
            CompanyService.getCompanyInfo($scope.target).then(function(response) {
                $scope.client = response;
            });
        }

        PeriodDefinitionRepository.query().$promise.then(function(payPeriods){
          $scope.payPeriods = payPeriods;
        });

        // Define a default behavior when no function parameter is given
        if (!$attrs.exitView) {
            $scope.exitView = function() {
                $window.history.back();
            };
        }

        $scope.saveCompanyInfo = function(){
          CompanyService.saveCompanyInfo($scope.client).then(function(response) {
            alert('Changes saved successfully');
            $scope.exitView();
          }, function(error) {
            alert("Failed to add client. " + error);
          })
        };

        $scope.cancel = function() {
            $scope.exitView();
        };

        $scope.isNewCompany = function() {
          return !$scope.target;
        };
    }
  ];

  return {
    restrict: 'E',
    scope: {
        target: '=?',
        exitView: '&'
    },
    templateUrl: '/static/partials/common/directive_company_info_edit.html',
    controller: controller
  };
});
