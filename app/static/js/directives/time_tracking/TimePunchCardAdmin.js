BenefitMyApp.controller('TimePunchCardWeeklyViewModalController', [
  '$scope',
  '$modalInstance',
  'week',
  'user',
  'companyId',
  'adminMode',
  function(
    $scope,
    $modalInstance,
    week,
    user,
    companyId,
    adminMode) {

    $scope.week = week;
    $scope.user = user;
    $scope.companyId = companyId;
    $scope.adminMode = adminMode;

    $scope.close = function(){
        $modalInstance.close();
    };
  }
]).controller('TimePunchCardAdminController', [
    '$scope',
    '$state',
    '$modal',
    '$attrs',
    '$controller',
    'UserService',
    'utilityService',
    'DateTimeService',
    'TimePunchCardService',
    'CompanyEmployeeSummaryService',
    'CompanyPersonnelsService',
    'EmployeeProfileService',
    function TimePunchCardAdminController(
      $scope,
      $state,
      $modal,
      $attrs,
      $controller,
      UserService,
      utilityService,
      DateTimeService,
      TimePunchCardService,
      CompanyEmployeeSummaryService,
      CompanyPersonnelsService,
      EmployeeProfileService) {

        // Inherite scope from base
        $controller('modalMessageControllerBase', {$scope: $scope});

        $scope.$watch('company', function(watchedArray) {
          // Configuration of the view window of weeks to include
          var preWeeks = 10;
          var postWeeks = 5;

          // Populate the weeks for display
          $scope.listOfWeeks = DateTimeService.GetListOfWeeks(preWeeks, postWeeks);

          $scope.selectedDisplayWeek = _.find($scope.listOfWeeks, function(weekItem) {
              return weekItem.isCurrentWeek;
          });

          $scope.reloadTimePunchCard();
          
        });

        $scope.isAllCompanyView = function(){
          return _.isUndefined($scope.manangerUser);
        };

        $scope.reloadTimePunchCard = function() {
          var employeePromise;
          if($scope.company){
            if($scope.isAllCompanyView()){
              employeePromise = CompanyPersonnelsService.getCompanyEmployees($scope.company.id);
            }
            else{
              employeePromise = CompanyPersonnelsService.getEmployeeDirectReports($scope.company.id, $scope.manangerUser.id);
            }
          }

          if (!employeePromise){
            return;
          }

          TimePunchCardService.GetPunchCardsByCompanyTimeRange($scope.company.id, $scope.selectedDisplayWeek.weekStartDate, true)
          .then(function(companyPunchCardsByEmployee) {

            // Expect companyPunchCardsByEmployee is an array of objects
            // which keys off employee person descriptor (user id)
            var employeeTotalTimes = [];
            var employees = _.keys(companyPunchCardsByEmployee);

            employeePromise.then(function(employeeListBuilder) {
              employeeListBuilder.filterByTimeRangeStatus(
                null,
                EmployeeProfileService.EmploymentStatuses.Terminated,
                $scope.selectedDisplayWeek.weekStartDate,
                moment($scope.selectedDisplayWeek.weekStartDate).add(7, 'days')
              );
              employeeListBuilder.orderByLastName();

              _.each(employeeListBuilder.list, function(employee) {
                if(!$scope.firstEmployee){
                  $scope.firstEmployee = employee;
                }
                // Convert to environment aware user id for employee comparison
                var envAwareUserId = utilityService.getEnvAwareId(employee.user.id);

                // if employee has not filed any punch card
                if (!_.contains(employees, envAwareUserId)) {
                  var blankPunchCard = TimePunchCardService.GetBlankPunchCardForEmployeeUser(
                    employee.user,
                    $scope.company.id,
                    $scope.selectedDisplayWeek.weekStartDate
                  );

                  blankPunchCard.hours = 0;
                  employeeTotalTimes.push(blankPunchCard);
                } else {
                  var employeePunchCards = companyPunchCardsByEmployee[envAwareUserId];

                  if (employeePunchCards && employeePunchCards.length > 0) {
                    var totalTimeInHour = TimePunchCardService.CalculateTotalHours(employeePunchCards);
                    var isInProgress = TimePunchCardService.HasInProgressPunchCards(employeePunchCards);
                    // Get employee information from the first punch time
                    employeeTotalTimes.push({
                      employee: employeePunchCards[0].employee,
                      isInProgress: isInProgress,
                      hours: totalTimeInHour.toFixed(2)
                    });
                  }
                }
              });

              $scope.employeePunchCards = employeeTotalTimes;
            });
          });
        };


        $scope.downloadWeeklyTimePunchCardReport = function() {
            var link = CompanyEmployeeSummaryService.getWeeklyTimePunchCardReportUrl(
            $scope.company.id,
            $scope.selectedDisplayWeek.weekStartDate);

            location.href = link;
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
                },
                'adminMode': function(){
                  return true;
                }
              }
            });

            modalInstance.result.then(function() {
              $scope.reloadTimePunchCard();
            });
          });
        };

        $scope.editIndividual = function(){  
          $state.go('admin_individual_timepunchcards',
            {
              employee_id: $scope.firstEmployee.user.id,
              startDate: $scope.selectedDisplayWeek.weekStartDate
            }
          );
        };
    }
  ]
).directive('bmTimePunchCardAdmin', function() {
  return {
    restrict: 'E',
    scope: {
        company: '=',
        manangerUser: '='
    },
    templateUrl: '/static/partials/time_punch_card/directive_time_punch_card_admin.html',
    controller: 'TimePunchCardAdminController'
  };
});
