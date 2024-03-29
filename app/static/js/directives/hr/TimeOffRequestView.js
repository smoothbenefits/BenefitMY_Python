BenefitMyApp.controller('TimeOffRequestModalController', [
  '$scope', '$modalInstance', 'user', 'manager', 'companyId', 'TimeOffService',
  function($scope, $modalInstance, user, manager, companyId, TimeOffService){

    if (!manager.isHr) {
      $scope.approverName = manager.first_name + ' ' + manager.last_name;
    } else {
      $scope.approverName = 'No manager found in the system. ' +
        'Request will be directed to ' + manager.first_name + ' ' + manager.last_name;
    }

    $scope.timeoffTypes = TimeOffService.GetAvailableTimeoffTypes();

    $scope.timeoff = {
      'approver': manager,
      'requestor': user
    };

    $scope.timeoff.requestor.companyId = companyId;

    $scope.cancel = function() {
      $modalInstance.dismiss();
    };

    $scope.save = function() {

      TimeOffService.RequestTimeOff($scope.timeoff).then(function(savedRequest) {
        $modalInstance.close(true);
      }, function(error) {
        $modalInstance.close(false);
      })
    }
  }
]).controller('TimeOffRequestViewDirectiveController', [
  '$scope',
  '$state',
  '$modal',
  '$controller',
  'EmployeeProfileService',
  'PersonService',
  'TimeOffService',
  'CompanyService',
  function($scope,
           $state,
           $modal,
           $controller,
           EmployeeProfileService,
           PersonService,
           TimeOffService,
           CompanyService){

    // Inherite scope from base
    $controller('modalMessageControllerBase', {$scope: $scope});

    $scope.hasPendingRequests = function() {
        return $scope.pendingRequests && $scope.pendingRequests.length;
    };

    $scope.hasDecidedRequests = function() {
        return $scope.decidedRequests && $scope.decidedRequests.length;
    };

    $scope.$watch('user', function(theUser){
      if(theUser){
        $scope.user = theUser;
        // Get existing time off requests
        TimeOffService.GetTimeOffsByRequestor(theUser.id)
        .then(function(timeOffs) {
          if (timeOffs) {
            $scope.pendingRequests = _.filter(timeOffs, function(request) {
                return request.status == TimeOffService.TimeoffStatus.Pending;
            });
            $scope.decidedRequests = _.filter(timeOffs, function(request) {
                return request.status != TimeOffService.TimeoffStatus.Pending;
            });
          }
        });

        var companyId = theUser.company_group_user[0].company_group.company.id;

        TimeOffService.GetTimeOffQuota(theUser.id, companyId)
        .then(function(quotaData){
          $scope.quotaData = quotaData;
        });

        // Get manager information through employee profile
        EmployeeProfileService.getEmployeeProfileForCompanyUser(companyId, theUser.id)
        .then(function(profile) {
          $scope.employeeProfile = profile;
          return profile.manager;
        }).then(function(manager){

          // If manager not defined, redirect requests to company HR admin
          if (!manager) {
            CompanyService.getCompanyAdmin(companyId).then(function(admins) {
              $scope.employeeProfile.manager = admins[0];
              $scope.employeeProfile.manager.userId = $scope.employeeProfile.manager.id;
              $scope.employeeProfile.manager.isHr = true;

              // Use the HR's person profile email for timeoff request communication
              PersonService.getSelfPersonInfo($scope.employeeProfile.manager.userId)
                .then(function(person) {
                  if (person) {
                    $scope.employeeProfile.manager.email = person.email;
                  }
                });
            });
          } else {
            PersonService.getSelfPersonInfoByPersonId(manager.person)
            .then(function(person) {
              $scope.employeeProfile.manager.userId = person.person.user;
              $scope.employeeProfile.manager.email = person.person.email;
            });
          }
        });
      }
    });

    $scope.showQuotaInfo = function() {
        return $scope.quotaData 
            && $scope.quotaData.quotaInfoCollection
            && $scope.quotaData.quotaInfoCollection.length > 0;
    };

    $scope.cancelRequest = function(timeoffRequest) {
        var confirmMessage = 'Are you sure you want to cancel the time off request?';
        if (confirm(confirmMessage)) {
            TimeOffService.UpdateTimeOffStatus(timeoffRequest, TimeOffService.TimeoffStatus.Canceled)
            .then(function(updatedRequest){
              $scope.pendingRequests = 
                _.reject($scope.pendingRequests, {id:updatedRequest.id});
              $scope.decidedRequests.unshift(updatedRequest);
            });
        }
    };

    $scope.requestTimeOff = function(){
      var modalInstance = $modal.open({
        templateUrl: '/static/partials/timeoff/modal_request_timeoff.html',
        controller: 'TimeOffRequestModalController',
        size: 'lg',
        backdrop: 'static',
        resolve: {
          'user': function() {
            return $scope.user;
          },
          'manager': function() {
            return $scope.employeeProfile.manager;
          },
          'companyId': function() {
            return $scope.employeeProfile.companyId;
          }
        }
      });

      modalInstance.result.then(function(success){
        if (success){
          var successMessage = "Your timeoff request has been saved. " +
          "You can return to dashboard through left navigation panel. " +
          "Or create another request.";

          $scope.showMessageWithOkayOnly('Success', successMessage);
        } else{
          var message = 'Failed to save time off request. Please try again later.';
          $scope.showMessageWithOkayOnly('Error', message);
        }

        $state.reload();
      });

    };
  }
]).directive('bmTimeOffRequestor', function(){

    return {
        restrict: 'E',
        scope: {
          user: '='        
        },
        templateUrl: '/static/partials/timeoff/directive_time_off_request_view.html',
        controller: 'TimeOffRequestViewDirectiveController'
      };
});