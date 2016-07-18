BenefitMyApp.controller('TimePunchCardController', [
    '$scope',
    '$modal',
    '$attrs',
    '$controller',
    function TimePunchCardController(
      $scope,
      $modal,
      $attrs,
      $controller) {

        // Inherite scope from base
        $controller('modalMessageControllerBase', {$scope: $scope});

        /**
            Get the list of weeks for display
        */
        var getListOfWeeks = function() {

            // Configuration of the view window of weeks to include
            var preWeeks = 10;
            var postWeeks = 5;

            var weeks = [];

            // Get the start date of the current week as reference
            var today = moment();
            var startDateOfCurrentWeek = moment(today).startOf('week');

            // Construct the list of weeks and massage the data ready for
            // display
            for (var i = -preWeeks; i <= postWeeks; i++) {
                var weekStartDate = moment(startDateOfCurrentWeek).add(i, 'weeks');
                var weekEndDate = moment(weekStartDate).endOf('week');
                var weekItem = {
                    weekStartDate: weekStartDate,
                    weekDisplayText: weekStartDate.format(SHORT_DATE_FORMAT_STRING)
                                    + ' - '
                                    + weekEndDate.format(SHORT_DATE_FORMAT_STRING)
                };

                // Mark the current week for easy selection
                if (weekItem.weekStartDate.isSame(startDateOfCurrentWeek)) {
                    weekItem.isCurrentWeek = true;
                    weekItem.weekDisplayText = weekItem.weekDisplayText + ' [*]'
                }

                weeks.push(weekItem);
            }

            return weeks;
        };

        $scope.$watchGroup(['user', 'company'], function(watchGroup) {
          if(watchGroup && watchGroup[0] && watchGroup[1]){
            // Populate the weeks for display
            $scope.listOfWeeks = getListOfWeeks();

            $scope.selectedDisplayWeek = _.find($scope.listOfWeeks, function(weekItem) {
                return weekItem.isCurrentWeek;
            });

            $scope.reloadTimePunchCard();
          }
        });

        $scope.reloadTimePunchCard = function() {
        };
    }
  ]
).directive('bmTimePunchCard', function() {
  return {
    restrict: 'E',
    scope: {
        user: '=',
        company: '='
    },
    templateUrl: '/static/partials/time_punch_card_new/directive_time_punch_card.html',
    controller: 'TimePunchCardController'
  };
});
