BenefitMyApp.controller('CompanyTimeOffViewDirectiveController', [
  '$scope',
  '$state',
  'EmployeeProfileService',
  'PersonService',
  'TimeOffService',
  'CompanyService',
  function($scope,
           $state,
           EmployeeProfileService,
           PersonService,
           TimeOffService,
           CompanyService){

    $scope.hasPendingRequests = function() {
        return $scope.pendingRequests && $scope.pendingRequests.length;
    };

    $scope.hasDecidedRequests = function() {
        return $scope.decidedRequests && $scope.decidedRequests.length;
    };

    $scope.$watch('companyId', function(companyId){
      if(companyId){
        $scope.companyId = companyId;
        // Get existing time off requests
        TimeOffService.GetTimeOffsByCompany(companyId)
        .then(function(timeOffs) {
          if (timeOffs) {
            $scope.pendingRequests = timeOffs.requestsPending;
            $scope.decidedRequests = timeOffs.requestsActioned;
          }
        });
      }
    });
  }
]).directive('bmCompanyTimeOff', function(){

    return {
        restrict: 'E',
        scope: {
          companyId: '='        
        },
        templateUrl: '/static/partials/timeoff/directive_company_time_off_view.html',
        controller: 'CompanyTimeOffViewDirectiveController'
      };
});
