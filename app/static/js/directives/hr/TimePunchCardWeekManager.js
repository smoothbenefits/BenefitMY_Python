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

        $scope.init = function(){
          //The init function to setup all the initial state:
          $scope.allStates = UsStateService.GetAllStates();
          $scope.showSpinner = false;

          // Register the confirm message for saving timecard, so that the
          // auto confirm directive can use this properly.
          $scope.saveTimeCardsConfirmText =  'Do you want to proceed with submitting the TimeCard?';

          if($scope.adminMode){
              $scope.saveTimeCardsConfirmText = 'Do you really want to edit the timesheet for this employee?';
          }

          $scope.deleteTimeCardConfirm = 'Are you sure you want to delete this time sheet? The action cannot be reverted!';
          $scope.$watchGroup(['week', 'workPunchCard'], function(watchItems){
            if(watchItems[0]){
              var weekItem = watchItems[0];
              var startDate = weekItem.weekStartDate;
              $scope.datesOfWeek = [];
              for (var i=0; i<7; i++){
                var weekDate = moment(startDate).add(i, 'days');
                $scope.datesOfWeek[weekDate.format('dddd')] = weekDate;
              }
            }
            if(watchItems[1]){
              $scope.editMode = _.isUndefined($scope.workPunchCard.id);
              $scope.workHoursByStateList =
                WorkTimePunchCardService.GetWorkHoursByState($scope.workPunchCard);
            }
          });

          $scope.cardTypes = WorkTimePunchCardService.CARD_TYPES;
        };

        $scope.init();


        var getByStateTag = function(tags) {
          return _.find(tags, function(tag) {
            return tag.tagType === WorkTimePunchCardService.BY_STATE_PUNCHCARD_TYPE;
          });
        };

        $scope.displayDateByWeekday = function(weekday){
          if($scope.datesOfWeek){
            var weekDate = $scope.datesOfWeek[weekday];
            if(weekDate){
              return weekDate.format(SHORT_DATE_FORMAT_STRING);
            }
          }
          return '';
        }

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
          if(!byStateTag.tagContent || byStateTag.tagContent !== timecard.state){
            byStateTag.tagContent = timecard.state;
          }
        };


        $scope.isTimeCardValidForSave = function() {
          if (!$scope.workPunchCard) {
            return false;
          }
          var allNotApplicable = _.every($scope.workPunchCard.timecards, function(checkCards){
            var pairs = _.pairs(checkCards.workHours);
            return _.every(pairs, function(pair){
                return pair[1].notApplicable;
            });
          });

          return !allNotApplicable && _.every($scope.workPunchCard.timecards, function(timecard) {

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

              return pair[1].recordType !== $scope.cardTypes[0]
                || end.getTime() > start.getTime();
            });
          });
        };

        $scope.addTimeCard = function(){
          $scope.workPunchCard.timecards.push(WorkTimePunchCardService.GetBlankPunchCard());
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
                .then(function(resultPunchCards){
                    if($scope.saveResult){
                            $scope.saveResult({savedPunchCards: resultPunchCards});
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
                    function(resultPunchCards) {
                        if($scope.saveResult){
                            $scope.saveResult({savedPunchCards: resultPunchCards});
                        }
                        $scope.editMode = false;
                    },
                    function(errors) {
                        if($scope.saveResult){
                            $scope.saveResult();
                        }
                    }
                );
            }
        };

        $scope.cardTypeUpdated = function(timeCardOfWeekDay){
          timeCardOfWeekDay.notApplicable =
            WorkTimePunchCardService.IsHolidayRecordType(timeCardOfWeekDay.recordType);
        };

        $scope.showEdit = function(){
          $scope.editMode = true;
        };

        $scope.viewMode = function(){
          $scope.editMode = false;
        };
    }
  ]
).directive('bmTimePunchCardWeekManager', function() {
  return {
    restrict: 'E',
    scope: {
        adminMode: '=',
        workPunchCard: '=',
        week: '=',
        saveResult: '&'
    },
    templateUrl: '/static/partials/time_punch_card/directive_time_punch_card_week.html',
    controller: 'TimePunchCardWeekDirectiveController'
  };
});
