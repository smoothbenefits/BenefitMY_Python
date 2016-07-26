BenefitMyApp.controller('TimePunchCardWeeklyViewModalController', [
  '$scope',
  '$modalInstance',
  'week',
  'user',
  'company',
  function(
    $scope,
    $modalInstance,
    week,
    user,
    company) {

    $scope.week = week;
    $scope.user = user;
    $scope.company = company;

    $scope.close = function(){
        $modalInstance.close();
    };
  }
]).controller('TimePunchCardAdminController', [
    '$scope',
    '$modal',
    '$attrs',
    '$controller',
    'PersonService',
    'utilityService',
    'DateTimeService',
    'TimePunchCardService',
    function TimePunchCardAdminController(
      $scope,
      $modal,
      $attrs,
      $controller,
      PersonService,
      utilityService,
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

          TimePunchCardService.GetPunchCardsByCompanyTimeRange($scope.company.id, $scope.selectedDisplayWeek.weekStartDate)
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

        $scope.editTimeCard = function(employee, weekSelected) {

          var userId = utilityService.retrieveIdFromEnvAwareId(employee.personDescriptor);
          PersonService.getSelfPersonInfo(userId).then(function(person) {
            $modal.open({
              templateUrl: '/static/partials/time_punch_card/modal_weekly_time_punch_card.html',
              controller: 'TimePunchCardWeeklyViewModalController',
              size: 'lg',
              backdrop: 'static',
              resolve: {
                'week': function() {
                  return weekSelected;
                },
                'user': function() {
                  return person.person;
                },
                'company': function() {
                  return utilityService.retrieveIdFromEnvAwareId(employee.companyDescriptor);
                }
              }
            });
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
