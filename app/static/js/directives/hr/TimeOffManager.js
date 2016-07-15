BenefitMyApp.controller('TimeOffManagerDirectiveController', [
  '$scope',
  '$state',
  '$controller',
  'TimeOffService',
  function($scope,
           $state,
           $controller,
           TimeOffService){

    // Inherite scope from base
    $controller('modalMessageControllerBase', {$scope: $scope});

    $scope.hasDirectReportRequests = function() {
      return $scope.requestsFromDirectReports && $scope.requestsFromDirectReports.length;
    };

    $scope.hasActionedRequests = function(){
      return $scope.actionedRequests && $scope.actionedRequests.length;
    };

    $scope.$watchGroup(['user', 'company'], function(theWatched){
      var theUser = theWatched[0];
      var theCompany = theWatched[1];
      if(theUser){
        $scope.user = theUser;

        // Get time off requests awaiting the user's action
        TimeOffService.GetTimeOffsByApprover(theUser.id)
        .then(function(requests){
           $scope.requestsFromDirectReports = requests.requestsPending;
           $scope.actionedRequests = requests.requestsActioned;
        });
      }
      if(theCompany){
        TimeOffService.GetTimeOffQuotaByCompany(theCompany.id)
          .then(function(compQuotas){
            $scope.employeeQuotas = compQuotas;
          });
      }
    });

    $scope.getQuotaByTimeOffRequest = function(timeoffRequest){
      var personQuota = _.findWhere($scope.employeeQuotas,
                              {personDescriptor: timeoffRequest.requestor.personDescriptor});

      if(personQuota){
        var typeQuota = _.findWhere(personQuota.quotaInfoCollection,
                                    {timeoffType: timeoffRequest.type});
        if(typeQuota){
          return typeQuota.bankedHours;
        }
      }
      return 'N/A';
    };

    $scope.updateStatus = function(request, newStatus){
      var confirmMessage = 'Are you sure you want to approve the time off request?'
      if (newStatus === 'DENIED'){
        confirmMessage = 'Are you sure you want to deny the time off request?'
      }
      if(confirm(confirmMessage)){
        request.status = newStatus;
        TimeOffService.UpdateTimeOffStatus(request)
        .then(function(updatedRequest){
          $scope.requestsFromDirectReports = 
            _.reject($scope.requestsFromDirectReports, {id:updatedRequest.id});
          $scope.actionedRequests.unshift(updatedRequest);
        });
      }
    };
  }
]).directive('bmTimeOffManager', function(){

    return {
        restrict: 'E',
        scope: {
          user: '=',
          company: '='
        },
        templateUrl: '/static/partials/timeoff/directive_time_off_manager.html',
        controller: 'TimeOffManagerDirectiveController'
      };
});
