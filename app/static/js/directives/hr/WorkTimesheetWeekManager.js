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
                && _.isNumber($scope.timesheet.timecards[0].workHours.sunday.hours)
                && _.isNumber($scope.timesheet.timecards[0].workHours.monday.hours)
                && _.isNumber($scope.timesheet.timecards[0].workHours.tuesday.hours)
                && _.isNumber($scope.timesheet.timecards[0].workHours.wednesday.hours)
                && _.isNumber($scope.timesheet.timecards[0].workHours.thursday.hours)
                && _.isNumber($scope.timesheet.timecards[0].workHours.friday.hours)
                && _.isNumber($scope.timesheet.timecards[0].workHours.saturday.hours);
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
        adminMode: '=',
        timesheet: '=',
        saveResult: '&'
    },
    templateUrl: '/static/partials/work_timesheet/directive_work_timesheet_week.html',
    controller: 'WorkTimesheetWeekDirectiveController'
  };
});