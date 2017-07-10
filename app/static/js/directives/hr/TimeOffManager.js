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

    $scope.hasPendingRequests = function() {
      return $scope.pendingRequests && $scope.pendingRequests.length;
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
           $scope.pendingRequests = requests.requestsPending;
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

    $scope.denyRequest = function(request) {
        var confirmMessage = 'Are you sure you want to deny the time off request?';
        updateRequestStatus(request, TimeOffService.TimeoffStatus.Denied, confirmMessage);
    };

    $scope.approveRequest = function(request) {
        var confirmMessage = 'Are you sure you want to approve the time off request?';
        updateRequestStatus(request, TimeOffService.TimeoffStatus.Approved, confirmMessage);
    };

    $scope.revokeRequest = function(request) {
        var confirmMessage = 'Are you sure you want to revoke the approval issued on the time off request?\n\nThis will give the deducted hours back to the employee.';
        updateRequestStatus(request, TimeOffService.TimeoffStatus.Revoked, confirmMessage);
    };

    $scope.allowRevokeRequest = function(request) {
        return request.status == TimeOffService.TimeoffStatus.Approved;
    };

    var updateRequestStatus = function(request, newStatus, confirmMessage){
      if(confirm(confirmMessage)){
        TimeOffService.UpdateTimeOffStatus(request, newStatus)
        .then(
            function(updatedRequest) {
              $scope.pendingRequests = 
                _.reject($scope.pendingRequests, {id:updatedRequest.id});
              $scope.actionedRequests = 
                _.reject($scope.actionedRequests, {id:updatedRequest.id});
              $scope.actionedRequests.unshift(updatedRequest);
            },
            function(error) {
                alert('There was a problem updating the status of the timeoff request. Please try again later.');
            }
        );
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
