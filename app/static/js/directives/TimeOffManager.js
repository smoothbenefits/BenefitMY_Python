BenefitMyApp.controller('TimeoffRequestController', [
  '$scope', '$modalInstance', 'user', 'manager', 'TimeOffService',
  function($scope, $modalInstance, user, manager, TimeOffService){

    if (!manager.isHr) {
      $scope.approverName = manager.first_name + ' ' + manager.last_name;
    } else {
      $scope.approverName = 'No manager found in the system. ' +
        'Request will be directed to ' + manager.first_name + ' ' + manager.last_name;
    }

    $scope.timeoffTypes = [
      'Paid Time Off (PTO)',
      'Sick Day'
    ];

    $scope.timeoff = {
      'approver': manager,
      'requestor': user
    };

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
]).controller('TimeOffDirectiveController', [
  '$scope', '$state', '$modal', '$controller', 'EmployeeProfileService',
  'PersonService', 'TimeOffService', 'CompanyService',
  function($scope, $state, $modal, $controller, EmployeeProfileService,
           PersonService, TimeOffService, CompanyService){

    // Inherite scope from base
    $controller('modalMessageControllerBase', {$scope: $scope});

    $scope.$watch('user', function(theUser){
      if(theUser){

        TimeOffService.GetTimeOffsByRequestor(theUser.id)
        .then(function(timeOffs) {
          $scope.requestedTimeOffs = timeOffs;
        });

        var companyId = theUser.company_group_user[0].company_group.company.id;
        EmployeeProfileService.getEmployeeProfileForCompanyUser(companyId, theUser.id)
        .then(function(profile) {
          $scope.employeeProfile = profile;
          return profile.manager;
        }).then(function(manager){
          if (!manager) {
            CompanyService.getCompanyAdmin(companyId).then(function(admins) {
              $scope.employeeProfile.manager = admins[0];
              $scope.employeeProfile.manager.isHr = true;
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

    $scope.requestTimeOff = function(){
      var modalInstance = $modal.open({
        templateUrl: '/static/partials/timeoff/modal_request_timeoff.html',
        controller: 'TimeoffRequestController',
        size: 'lg',
        backdrop: 'static',
        resolve: {
          'user': function() {
            return $scope.user;
          },
          'manager': function() {
            return $scope.employeeProfile.manager;
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

    $scope.updateStatus = function(request, newStatus){
      if(confirm('Are you sure you want to ' + newStatus + ' the time off request?')){
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
        controller: 'TimeOffDirectiveController'
      };
});
