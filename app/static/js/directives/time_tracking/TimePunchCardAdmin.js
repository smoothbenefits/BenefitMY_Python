BenefitMyApp.controller('TimePunchCardWeeklyViewModalController', [
  '$scope',
  '$modalInstance',
  'week',
  function(
    $scope,
    $modalInstance,
    week) {

    $scope.week = week;

    $scope.close = function(){
        $modalInstance.close();
    };
  }
]).controller('TimePunchCardAdminController', [
    '$scope',
    '$modal',
    '$attrs',
    '$controller',
    'TimePunchCardService',
    function TimePunchCardAdminController(
      $scope,
      $modal,
      $attrs,
      $controller,
      TimePunchCardService) {

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

        $scope.$watch('company', function(company) {
          if(company){
            // Populate the weeks for display
            $scope.listOfWeeks = getListOfWeeks();

            $scope.selectedDisplayWeek = _.find($scope.listOfWeeks, function(weekItem) {
                return weekItem.isCurrentWeek;
            });

            $scope.reloadTimePunchCard();
          }
        });

        $scope.reloadTimePunchCard = function() {
          TimePunchCardService.GetWeeklyPunchCardsByCompany($scope.company.id, $scope.selectedDisplayWeek.weekStartDate)
          .then(function(companyPunchCardsByEmployee) {

            // Expect companyPunchCardsByEmployee is an array of objects
            // which key off employee person descriptor
            var employeeTotalTimes = [];
            var employees = _.keys(companyPunchCardsByEmployee);

            _.each(employees, function(employee) {
              var employeePunchCards = companyPunchCardsByEmployee[employee];

              if (employeePunchCards && employeePunchCards.length > 0) {
                // Calculate total time for each employee
                // Set initial reduce value to 0
                var totalTimeInHour = _.reduce(employeePunchCards, function(memo, punchCard) {
                  var startTime = moment(punchCard.start);
                  var endTime = moment(punchCard.end);

                  // Get time difference between start and end time in hour before rounding
                  var duration = endTime.diff(startTime, 'hours', true);

                  return memo + duration;
                }, 0);

                // Get employee information from the first punch time
                employeeTotalTimes.push({
                  employee: employeePunchCards[0].employee,
                  hours: totalTimeInHour.toFixed(2)
                });
              }
            });

            $scope.employeePunchCards = employeeTotalTimes;
          });
        };

        $scope.downloadWeeklyTimePunchCardReport = function() {
        };

        $scope.editTimeCard = function(userDesc, companyDesc, weekSelected) {
          $modal.open({
            templateUrl: '/static/partials/time_punch_card_new/modal_weekly_time_punch_card.html',
            controller: 'TimePunchCardWeeklyViewModalController',
            size: 'lg',
            backdrop: 'static',
            resolve: {
              'week': function() {
                return weekSelected;
              }
            }
          });
        };
    }
  ]
).directive('bmTimePunchCardAdmin', function() {
  return {
    restrict: 'E',
    scope: {
        company: '='
    },
    templateUrl: '/static/partials/time_punch_card/directive_time_punch_card_admin.html',
    controller: 'TimePunchCardAdminController'
  };
});
