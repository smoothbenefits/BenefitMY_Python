BenefitMyApp.controller('TimePunchCardWeekDirectiveController', [
    '$scope',
    '$attrs',
    '$controller',
    'WorkTimePunchCardService',
    'UsStateService',
    function TimePunchCardWeekDirectiveController(
      $scope,
      $attrs,
      $controller,
      WorkTimePunchCardService,
      UsStateService) {

        var curWeek = null;

        UsStateService.GetStates().then(function(allStates){
            $scope.allStates = allStates;
        });

        var getBlankPunchCardForWeek = function(week){
            var blankCard = WorkTimePunchCardService.GetBlankPunchCardForEmployeeUser(
                                $scope.user,
                                $scope.company,
                                week.weekStartDate);
            return blankCard;
        };

        var getByStateTag = function(tags) {
          return _.find(tags, function(tag) {
            return tag.tagType === WorkTimePunchCardService.BY_STATE_PUNCHCARD_TYPE;
          });
        };

        $scope.showSpinner = false;
        $scope.$watch('week', function(updatedWeek) {
            if(updatedWeek && curWeek !== updatedWeek){
                curWeek = updatedWeek;
                $scope.workPunchCard = getBlankPunchCardForWeek(updatedWeek);
            }
        });

        $scope.getTimeCardState = function(timecard) {
          var byStateTag = getByStateTag(timecard.tags);
          if (byStateTag) {
            return byStateTag.tagContent;
          } else {
            return null;
          }
        };

        $scope.stateSelected = function(timecard) {
          var byStateTag = getByStateTag(timecard.tags);
          byStateTag.tagContent = timecard.state;
        };

        // Register the confirm message for saving timecard, so that the
        // auto confirm directive can use this properly.
        $scope.saveTimeCardsConfirmText =  'Do you want to proceed with submitting the TimeCard?\n'
            + 'Please note once submitted, no further changes are allowed on this timesheet.';

        if($scope.adminMode){
            $scope.saveTimeCardsConfirmText = 'Do you really want to edit the timesheet for this employee?';
        }

        $scope.deleteTimeCardConfirm = 'Are you sure you want to delete this time sheet? The action cannot be reverted!';

        $scope.isTimeCardValidForSave = function() {
          if (!$scope.workPunchCard) {
            return false;
          }

          return _.every($scope.workPunchCard.timecards, function(timecard) {

            if (!timecard.state) {
              return false;
            }

            var pairs = _.pairs(timecard.workHours);
            return _.every(pairs, function(pair) {
              var start = pair[1].timeRange.start;
              var end = pair[1].timeRange.end;

              if (!start || !end) {
                return false;
              }

              return end.getTime() > start.getTime();
            });
          });
        };

        $scope.allowEdit = function() {
            return true;
        };

        $scope.addTimeCard = function(){
          var newPunchCard = getBlankPunchCardForWeek(curWeek);
          $scope.workPunchCard.timecards.push(newPunchCard.timecards[0]);
        };

        $scope.removeCard = function(timecard){
            $scope.workPunchCard.timecards = _.reject($scope.workPunchCard.timecards,
              function(candidate){
                return candidate == timecard;
            });
        };

        $scope.saveTimeCards = function() {
            if($scope.workPunchCard.id){
                WorkTimePunchCardService.UpdateWorkPunchCard($scope.workPunchCard)
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
                WorkTimePunchCardService.CreateWorkPunchCard($scope.workPunchCard)
                .then(
                    function(resultTimesheet) {
                        if($scope.saveResult){
                            $scope.saveResult({savedTimecards: resultTimesheet});
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
