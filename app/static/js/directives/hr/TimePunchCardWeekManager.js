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

        var curWeek = null;

        UsStateService.GetStates()
        .then(function(allStates){
            $scope.allStates = allStates;
        });

        var getBlankTimeCardForWeek = function(week){
            var blankCard = WorkTimesheetService.GetBlankTimesheetForEmployeeUser(
                                $scope.user,
                                $scope.company,
                                week.weekStartDate);
            blankCard.state = null;
            return blankCard;
        };

        $scope.showSpinner = false;
        $scope.$watch('week', function(updatedWeek) {
            if(updatedWeek && curWeek !== updatedWeek){
                curWeek = updatedWeek;
                $scope.timecards = [];
                $scope.timecards.push(getBlankTimeCardForWeek(updatedWeek));
            }
        });

        // Register the confirm message for saving timecard, so that the 
        // auto confirm directive can use this properly.
        $scope.saveTimeCardsConfirmText =  'Do you want to proceed with submitting the TimeCard?\n'
            + 'Please note once submitted, no further changes are allowed on this timesheet.';
        
        if($scope.adminMode){
            $scope.saveTimeCardsConfirmText = 'Do you really want to edit the timesheet for this employee?';
        }

        $scope.deleteTimeCardConfirm = 'Are you sure you want to delete this time sheet? The action cannot be reverted!';

        $scope.isTimeCardValidForSave = function() {
            return true;
        };

        $scope.allowEdit = function() {
            return true;
        };

        $scope.isTimeCardsValidForSave = function(){
            return false;
        };

        $scope.addTimeCard = function(){
            $scope.timecards.push(getBlankTimeCardForWeek(curWeek));
        };

        $scope.removeCard = function(timecard){
            $scope.timecards = _.reject($scope.timecards, function(candidate){
                return candidate == timecard;
            });
        };

        $scope.saveTimeCards = function() {
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
        user: '=',
        company: '=',
        saveResult: '&'
    },
    templateUrl: '/static/partials/time_punch_card/directive_time_punch_card_week.html',
    controller: 'TimePunchCardWeekDirectiveController'
  };
});