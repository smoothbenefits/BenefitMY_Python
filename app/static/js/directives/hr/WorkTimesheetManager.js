BenefitMyApp.controller('WorkTimeSheetEditModalController', [
  '$scope', '$modalInstance', 'user', 'timesheet', 'week', 'WorkTimesheetService',
  function($scope, $modalInstance, user, timesheet, week, WorkTimesheetService){
    $scope.timesheet = timesheet;
    $scope.week = week;
    $scope.adminMode = true;
    $scope.saveResult = function(savedTimesheet){
        $modalInstance.close(savedTimesheet);
    }
    $scope.dismiss = function() {
      $modalInstance.dismiss();
    };
  }
]).controller('WorkTimesheetManagerDirectiveController', [
    '$scope',
    '$modal',
    '$attrs',
    '$controller',
    'WorkTimesheetService',
    'CompanyPersonnelsService',
    'CompanyEmployeeSummaryService',
    function WorkTimesheetManagerDirectiveController(
      $scope,
      $modal,
      $attrs,
      $controller,
      WorkTimesheetService,
      CompanyPersonnelsService,
      CompanyEmployeeSummaryService) {

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

        $scope.reloadTimesheet = function() {
            WorkTimesheetService.GetWorkTimesheetByEmployeeUser(
                $scope.user,
                $scope.company,
                $scope.selectedDisplayWeek.weekStartDate)
            .then(function(timesheet) {
              $scope.timesheet = timesheet;
            });
            
            CompanyPersonnelsService.getCompanyEmployees($scope.company.id)
            .then(function(employees){
                WorkTimesheetService.GetWorkTimesheetsByCompany(
                    $scope.company.id,
                    $scope.selectedDisplayWeek.weekStartDate)
                .then(function(workTimeSheets){
                    $scope.employeeWorkHourList = [];
                    _.each(employees, function(employee){
                        var employeeWorksheet = _.find(workTimeSheets, function(timesheet){
                            return timesheet.employee.email == employee.user.email
                        });
                        if (!employeeWorksheet){
                            employeeWorksheet = 
                                WorkTimesheetService.GetBlankTimesheetForEmployeeUser(
                                    employee.user,
                                    $scope.company,
                                    $scope.selectedDisplayWeek.weekStartDate);
                        }
                        $scope.employeeWorkHourList.push(employeeWorksheet);
                    });
                });
            });
            
        };

        $scope.$watch('user', function(theUser) {
            if(theUser){
                // Populate the weeks for display
                $scope.listOfWeeks = getListOfWeeks();

                $scope.selectedDisplayWeek = _.find($scope.listOfWeeks, function(weekItem) {
                    return weekItem.isCurrentWeek;
                });

                // Now load the time sheet display based on the context
                $scope.reloadTimesheet();
            }
        });

        $scope.saveResult = function(savedTimeSheet){
            if(savedTimeSheet){
                $scope.reloadTimesheet();
                var successMessage = "Your work hour timesheet has been submitted successfully!"
                $scope.showMessageWithOkayOnly('Success', successMessage);
            }
            else{
                var message = 'Failed to save the timesheet. Please try again later.';
                $scope.showMessageWithOkayOnly('Error', message);
            }
        }

        $scope.viewDetails = function(timesheet){
            var modalInstance = $modal.open({
                templateUrl: '/static/partials/work_timesheet/modal_work_time_sheet.html',
                controller: 'WorkTimeSheetEditModalController',
                size: 'lg',
                backdrop: 'static',
                resolve: {
                  'user': function() {
                    return $scope.user;
                  },
                  'timesheet': function() {
                    return angular.copy(timesheet);
                  },
                  'week': function(){
                    return $scope.selectedDisplayWeek.weekDisplayText;
                  }
                }
              });

            modalInstance.result.then(function(savedTimesheet){
                $scope.reloadTimesheet();
            });
        };

        $scope.downloadWeeklyTimeSheetReport = function(){
          var link = CompanyEmployeeSummaryService.getWeeklyWorktimeReportUrl(
                $scope.company.id,
                $scope.selectedDisplayWeek.weekStartDate);
          location.href = link;
        };
    }
  ]
).directive('bmWorkTimesheetManager', function() {
  return {
    restrict: 'E',
    scope: {
        user: '=',
        adminMode: '=',
        company: '='
    },
    templateUrl: '/static/partials/work_timesheet/directive_work_timesheet_manager.html',
    controller: 'WorkTimesheetManagerDirectiveController'
  };
});
