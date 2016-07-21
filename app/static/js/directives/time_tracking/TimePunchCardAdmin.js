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
    'DateTimeService',
    'TimePunchCardService',
    function TimePunchCardAdminController(
      $scope,
      $modal,
      $attrs,
      $controller,
      DateTimeService,
      TimePunchCardService) {

        // Inherite scope from base
        $controller('modalMessageControllerBase', {$scope: $scope});

        $scope.$watch('company', function(company) {
          if(company){
            // Configuration of the view window of weeks to include
            var preWeeks = 10;
            var postWeeks = 5;

            // Populate the weeks for display
            $scope.listOfWeeks = DateTimeService.GetListOfWeeks(preWeeks, postWeeks);

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
            // which keys off employee person descriptor
            var employeeTotalTimes = [];
            var employees = _.keys(companyPunchCardsByEmployee);

            _.each(employees, function(employee) {
              var employeePunchCards = companyPunchCardsByEmployee[employee];

              if (employeePunchCards && employeePunchCards.length > 0) {
                var totalTimeInHour = TimePunchCardService.CalculateTotalHours(employeePunchCards);
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
