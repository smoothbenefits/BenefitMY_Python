BenefitMyApp.controller('TimeoffRequestController', [
  '$scope', '$modalInstance', 'user', 'manager',
  function($scope, $modalInstance, user, manager){

    $scope.timeoffTypes = [
      'Paid Time Off (PTO)',
      'Sick Day'
    ];

    $scope.approverName = function() {
      if (manager) {
        return manager.first_name + ' ' + manager.last_name;
      }
      return 'No manager found in the system.';
    };

    $scope.timeoff = {
      'approver': manager
    };

    $scope.cancel = function() {
      $modalInstance.dismiss();
    };

    $scope.save = function() {

    }
  }
]).controller('TimeOffDirectiveController', [
  '$scope', '$state', '$modal', 'TimeOffService', 'EmployeeProfileService',
  'PersonService',
  function($scope, $state, $modal, TimeOffService, EmployeeProfileService,
           PersonService){
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

      modalInstance.result.then(function(account){
        var successMessage = "Your timeoff request has been saved. " +
              "You can return to dashboard through left navigation panel. " +
              "Or create another request.";

        $scope.showMessageWithOkayOnly('Success', successMessage);

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
