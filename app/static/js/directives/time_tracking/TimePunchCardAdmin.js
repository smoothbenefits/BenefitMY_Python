BenefitMyApp.controller('TimePunchCardWeeklyViewModalController', [
  '$scope',
  '$modalInstance',
  'week',
  'user',
  'companyId',
  function(
    $scope,
    $modalInstance,
    week,
    user,
    companyId) {

    $scope.week = week;
    $scope.user = user;
    $scope.companyId = companyId;

    $scope.close = function(){
        $modalInstance.close();
    };
  }
]).controller('TimePunchCardAdminController', [
    '$scope',
    '$modal',
    '$attrs',
    '$controller',
    'UserService',
    'utilityService',
    'DateTimeService',
    'TimePunchCardService',
    'CompanyPersonnelsService',
    function TimePunchCardAdminController(
      $scope,
      $modal,
      $attrs,
      $controller,
      UserService,
      utilityService,
      DateTimeService,
      TimePunchCardService,
      CompanyPersonnelsService) {

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

          var employeePromise = CompanyPersonnelsService.getCompanyEmployees($scope.company.id);

          TimePunchCardService.GetPunchCardsByCompanyTimeRange($scope.company.id, $scope.selectedDisplayWeek.weekStartDate)
          .then(function(companyPunchCardsByEmployee) {

            // Expect companyPunchCardsByEmployee is an array of objects
            // which keys off employee person descriptor (user id)
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

            var countedEmployees = _.map(employeeTotalTimes, function(times) {
              return times.employee.personDescriptor;
            });

            // Get all employees in the company and fill in 0s for employees
            // who have not filed any punch card yet
            employeePromise.then(function(allEmployees) {
              _.each(allEmployees, function(employee) {

                // Convert to environment aware user id for employee comparison
                var envAwareUserId = utilityService.getEnvAwareId(employee.user.id);
                if (!_.contains(countedEmployees, envAwareUserId)) {
                  employeeTotalTimes.push({
                    employee: {
                      personDescriptor: envAwareUserId,
                      companyDescriptor: utilityService.getEnvAwareId($scope.company.id),
                      firstName: employee.user.first_name,
                      lastName: employee.user.last_name
                    },
                    hours: 0
                  });
                  countedEmployees.push(envAwareUserId);
                }
              });

              $scope.employeePunchCards = employeeTotalTimes;
            });
          });
        };

        $scope.downloadWeeklyTimePunchCardReport = function() {
        };

        $scope.editTimeCard = function(employee, weekSelected) {

          var userId = utilityService.retrieveIdFromEnvAwareId(employee.personDescriptor);

          UserService.getUserDataByUserId(userId).then(function(user) {
            var modalInstance = $modal.open({
              templateUrl: '/static/partials/time_punch_card/modal_weekly_time_punch_card.html',
              controller: 'TimePunchCardWeeklyViewModalController',
              size: 'lg',
              backdrop: 'static',
              resolve: {
                'week': function() {
                  return weekSelected;
                },
                'user': function() {
                  return user;
                },
                'companyId': function() {
                  return utilityService.retrieveIdFromEnvAwareId(employee.companyDescriptor);
                }
              }
            });

            modalInstance.result.then(function() {
              $scope.reloadTimePunchCard();
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
