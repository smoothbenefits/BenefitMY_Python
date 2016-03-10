BenefitMyApp.controller('TimePunchCardWeekDirectiveController', [
    '$scope',
    '$attrs',
    '$controller',
    'WorkTimesheetService',
    'UsStateService',
    function TimePunchCardWeekDirectiveController(
      $scope,
      $attrs,
      $controller,
      WorkTimesheetService,
      UsStateService) {

        $scope.allowEdit = function() {
            return true;
        };

        UsStateService.GetStates()
            .then(function(allStates){
                $scope.allStates = allStates;
            });

        $scope.isTimeCardValidForSave = function() {
            return true;
        };


        // Register the confirm message for saving timecard, so that the 
        // auto confirm directive can use this properly.
        $scope.saveTimecardConfirmText =  'Do you want to proceed with submitting the TimeCard?\n'
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
).directive('bmTimePunchCardWeekManager', function() {
  return {
    restrict: 'E',
    scope: {
        adminMode: '=',
        week: '=',
        saveResult: '&'
    },
    templateUrl: '/static/partials/time_punch_card/directive_time_punch_card_week.html',
    controller: 'TimePunchCardWeekDirectiveController'
  };
});