BenefitMyApp.controller('TimeOffManagerDirectiveController', [
  '$scope',
  '$state',
  '$controller',
  'EmployeeProfileService',
  'PersonService',
  'TimeOffService',
  'CompanyService',
  function($scope,
           $state,
           $controller,
           EmployeeProfileService,
           PersonService,
           TimeOffService,
           CompanyService){

    // Inherite scope from base
    $controller('modalMessageControllerBase', {$scope: $scope});

    $scope.hasDirectReportRequests = function() {
      return $scope.requestsFromDirectReports && $scope.requestsFromDirectReports.length;
    };

    $scope.$watch('user', function(theUser){
      if(theUser){
        $scope.user = theUser;

        // Get time off requests awaiting the user's action
        TimeOffService.GetTimeOffsByApprover(theUser.id)
        .then(function(requests){
           $scope.requestsFromDirectReports = requests;
        });
      }
    });

    $scope.updateStatus = function(request, newStatus){
      var confirmMessage = 'Are you sure you want to approve the time off request?'
      if (newStatus === 'DENIED'){
        confirmMessage = 'Are you sure you want to deny the time off request?'
      }
      if(confirm(confirmMessage)){
        request.status = newStatus;
        TimeOffService.UpdateTimeOffStatus(request)
        .then(function(updatedRequest){
          _.each($scope.requestsFromDirectReports, function(request, idx){
            if(updatedRequest.id == request.id){
              $scope.requestsFromDirectReports[idx] = updatedRequest;
            }
          })
        });
      }
    };
  }
]).directive('bmTimeOffManager', function(){

    return {
        restrict: 'E',
        scope: {
          user: '='
        },
        templateUrl: '/static/partials/timeoff/directive_time_off_manager.html',
        controller: 'TimeOffManagerDirectiveController'
      };
});
