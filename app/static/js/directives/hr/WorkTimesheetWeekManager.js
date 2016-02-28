BenefitMyApp.controller('WorkTimesheetWeekDirectiveController', [
    '$scope',
    '$attrs',
    '$controller',
    'WorkTimesheetService',
    function WorkTimesheetWeekDirectiveController(
      $scope,
      $attrs,
      $controller,
      WorkTimesheetService) {

        $scope.allowEdit = function() {
            return $scope.timesheet
                && !$scope.timesheet.id;
        };

        $scope.isTimesheetValidForSave = function() {
            return $scope.timesheet
                && !$scope.timesheet.id
                && _.isNumber($scope.timesheet.workHours.sunday)
                && _.isNumber($scope.timesheet.workHours.monday)
                && _.isNumber($scope.timesheet.workHours.tuesday)
                && _.isNumber($scope.timesheet.workHours.wednesday)
                && _.isNumber($scope.timesheet.workHours.thursday)
                && _.isNumber($scope.timesheet.workHours.friday)
                && _.isNumber($scope.timesheet.workHours.saturday);
        };


        // Register the confirm message for saving timesheet, so that the 
        // auto confirm directive can use this properly.
        $scope.saveTimesheetConfirmText =  'Do you want to proceed with submitting the timesheet?\n'
            + 'Please note once submitted, no further changes are allowed on this timesheet.';

        $scope.save = function(){
            if ($scope.saveTimesheet){
                $scope.saveTimesheet();
            }
        };
    }
  ]
).directive('bmWorkTimesheetWeekManager', function() {
  return {
    restrict: 'E',
    scope: {
        user: '=*',
        adminMode: '=',
        week: '=*',
        timesheet: '=*',
        saveTimesheet: '&'
    },
    templateUrl: '/static/partials/work_timesheet/directive_work_timesheet_week.html',
    controller: 'WorkTimesheetWeekDirectiveController'
  };
});