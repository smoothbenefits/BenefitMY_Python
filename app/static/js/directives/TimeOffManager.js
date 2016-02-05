BenefitMyApp.controller('TimeoffRequestController', [
  '$scope', '$modalInstance', 'user', 'manager', 'TimeOffService',
  function($scope, $modalInstance, user, manager, TimeOffService){

    if (manager) {
      $scope.approverName = manager.first_name + ' ' + manager.last_name;
    } else {
      $scope.approverName = 'No manager found in the system.';
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
      if (!manager && (!$scope.alt_approver_first_name || !$scope.alt_approver_last_name
        || !$scope.alt_approver_email)) {

        alert("Alternative approver's name and email are needed.");
        return;
      }

      TimeOffService.RequestTimeOff($scope.timeoff).then(function(savedRequest) {
        $modalInstance.close(true);
      }, function(error) {
        $modalInstance.close(false);
      })
    }
  }
]).controller('TimeOffDirectiveController', [
  '$scope', '$state', '$modal', '$controller', 'EmployeeProfileService',
  'PersonService', 'TimeOffService',
  function($scope, $state, $modal, $controller, EmployeeProfileService,
           PersonService, TimeOffService){

    // Inherite scope from base
    $controller('modalMessageControllerBase', {$scope: $scope});

    $scope.$watch('user', function(theUser){
      if(theUser){
        TimeOffService.GetTimeOffsByRequestor(theUser.id)
        .then(function(timeOffs){
          $scope.requestedTimeOffs = timeOffs;
        });

        var companyId = theUser.company_group_user[0].company_group.company.id;
        EmployeeProfileService.getEmployeeProfileForCompanyUser(companyId, theUser.id)
        .then(function(profile) {
          $scope.employeeProfile = profile;
          return profile.manager;
        }).then(function(manager){
          if (!manager) {
            return None;
          } else {
            PersonService.getSelfPersonInfoByPersonId(manager.person)
            .then(function(person) {
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

        $state.refresh();
      });
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
})
