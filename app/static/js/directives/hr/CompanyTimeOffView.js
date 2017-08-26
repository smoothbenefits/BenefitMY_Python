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
    $scope.startDate = moment().subtract(7, 'days').format('L');
    $scope.endDate = moment().format('L');
    $scope.$watch('companyId', function(companyId){
      if(companyId){
        $scope.companyId = companyId;
        // Get existing time off requests
        TimeOffService.GetTimeOffsByCompany(companyId, $scope.startDate, $scope.endDate)
        .then(function(timeOffs) {
          if (timeOffs) {
            $scope.pendingRequests = timeOffs.requestsPending;
            $scope.decidedRequests = timeOffs.requestsActioned;
          }
        });
      }
    });

    $scope.$watchGroup(['startDate', 'endDate'], function(group){
      if(moment($scope.startDate) >= moment($scope.endDate)){
        $scope.errorMessage = "The Start Date cannot be the same or later than End Date";
      }
      else if($scope.companyId){
        $scope.errorMessage = null;
        // Get existing time off requests
        TimeOffService.GetTimeOffsByCompany($scope.companyId, moment($scope.startDate), moment($scope.endDate))
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
