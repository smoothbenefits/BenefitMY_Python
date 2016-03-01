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
            return $scope.adminMode || 
                $scope.timesheet && !$scope.timesheet.id;
        };

        $scope.isTimesheetValidForSave = function() {
            return $scope.timesheet
                && ($scope.adminMode || !$scope.timesheet.id)
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
        
        if($scope.adminMode){
            $scope.saveTimesheetConfirmText = 'Do you really want to edit the timesheet for this employee?';
        }

        $scope.saveTimesheet = function() {
            if($scope.timesheet.id){
                WorkTimesheetService.UpdateWorkTimesheet($scope.timesheet)
                .then(function(resultTimesheet){
                    if($scope.saveResult){
                            $scope.saveResult({savedTimeSheet: resultTimesheet});
                        }
                    }, function(errors){
                        if($scope.saveResult){
                            $scope.saveResult();
                        }
                    }
                );
            }
            else{
                WorkTimesheetService.CreateWorkTimesheet($scope.timesheet)
                .then(
                    function(resultTimesheet) {
                        if($scope.saveResult){
                            $scope.saveResult({savedTimeSheet: resultTimesheet});
                        }
                    },
                    function(errors) {
                        if($scope.saveResult){
                            $scope.saveResult();
                        }
                    }
                );
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
        saveResult: '&'
    },
    templateUrl: '/static/partials/work_timesheet/directive_work_timesheet_week.html',
    controller: 'WorkTimesheetWeekDirectiveController'
  };
});