BenefitMyApp.directive('bmCompanyInfoEditor', function() {

  var controller = [
    '$scope',
    '$location',
    '$window',
    '$attrs',
    'CompanyService',
    'PeriodDefinitionRepository',
    'MonthsInYear',
    function CompanyInfoEditorDirectiveController(
      $scope,
      $location,
      $window,
      $attrs,
      CompanyService,
      PeriodDefinitionRepository,
      MonthsInYear) {

        $scope.client = {};

        if ($scope.target) {
            CompanyService.getCompanyInfo($scope.target).then(function(response) {
                $scope.client = response;
            });
        }

        PeriodDefinitionRepository.query().$promise.then(function(payPeriods){
          $scope.payPeriods = payPeriods;
        });

        $scope.monthsInYear = MonthsInYear;
        var day = 1;
        $scope.daysInMonth = [];
        while(day <= moment().month(0).daysInMonth()){
          $scope.daysInMonth.push(day++);
        }

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
          return !$scope.client.company || !$scope.client.company.id;
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
