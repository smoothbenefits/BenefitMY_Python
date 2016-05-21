BenefitMyApp.controller('WorkTimesheetWeekDirectiveController', [
    '$scope',
    '$attrs',
    '$controller',
    'WorkTimesheetService',
    'UsStateService',
    function WorkTimesheetWeekDirectiveController(
      $scope,
      $attrs,
      $controller,
      WorkTimesheetService,
      UsStateService) {

        $scope.allowEdit = function() {
            return $scope.adminMode || 
                $scope.timesheet && !$scope.timesheet.id;
        };

        $scope.allStates = UsStateService.GetAllStates();

        $scope.getTimeCardState = function(timecard) {
          var byStateTag = WorkTimesheetService.GetByStateTag(timecard.tags);
          if (byStateTag) {
            return byStateTag.tagContent;
          } else {
            return null;
          }
        };
        $scope.stateSelected = function(timecard) {
          var byStateTag = WorkTimesheetService.GetByStateTag(timecard.tags);
          if(!byStateTag.tagContent || byStateTag.tagContent !== timecard.state){
            byStateTag.tagContent = timecard.state;
          }
        };

        $scope.isTimesheetValidForSave = function() {
            return $scope.timesheet
                && ($scope.adminMode || !$scope.timesheet.id)
                && _.every($scope.timesheet.timecards, function(timecard) {
                    if (!timecard.state) {
                      return false;
                    }
                    else
                    {
                        return _.isNumber(timecard.workHours.sunday.hours)
                            && _.isNumber(timecard.workHours.monday.hours)
                            && _.isNumber(timecard.workHours.tuesday.hours)
                            && _.isNumber(timecard.workHours.wednesday.hours)
                            && _.isNumber(timecard.workHours.thursday.hours)
                            && _.isNumber(timecard.workHours.friday.hours)
                            && _.isNumber(timecard.workHours.saturday.hours);
                    }
                });
        };

        $scope.addTimeCard = function(){
          $scope.timesheet.timecards.push(WorkTimesheetService.GetBlankTimecard());
        };

        $scope.removeCard = function(timecard){
            $scope.timesheet.timecards = _.reject($scope.timesheet.timecards,
              function(candidate){
                return candidate == timecard;
            });
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