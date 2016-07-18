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
    function TimePunchCardAdminController(
      $scope,
      $modal,
      $attrs,
      $controller) {

        /**
            #####################
            #  Fake Data Begin
            #####################
        */

        $scope.employeeTimeCards = [
            {
                'employee': {
                    'firstName': 'Simon',
                    'lastName': 'Cowell'
                },
                'getTotalBaseHours': function() {
                    return 40;
                },
                updatedTimestamp: 'Tuesday, July 5, 2016 8:08 PM'
            },
            {
                'employee': {
                    'firstName': 'Clint',
                    'lastName': 'Wilson'
                },
                'getTotalBaseHours': function() {
                    return 38.5;
                },
                updatedTimestamp: 'Monday, July 4, 2016 4:08 PM'
            },
            {
                'employee': {
                    'firstName': 'Laura',
                    'lastName': 'White'
                },
                'getTotalBaseHours': function() {
                    return 47.5;
                },
                updatedTimestamp: 'Thursday, July 7, 2016 11:25 AM'
            }
        ];

        /**
            #####################
            #  Fake Data End
            #####################
        */

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
    templateUrl: '/static/partials/time_punch_card_new/directive_time_punch_card_admin.html',
    controller: 'TimePunchCardAdminController'
  };
});
