BenefitMyApp.directive('bmWorkTimesheetManager', function() {

  var controller = [
    '$scope',
    '$modal',
    '$attrs',
    '$controller',
    'WorkTimesheetService',
    function WorkTimesheetManagerDirectiveController(
      $scope,
      $modal,
      $attrs,
      $controller,
      WorkTimesheetService) {

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

        $scope.isTimesheetValidForSave = function() {
            return $scope.timesheet
                && !$scope.timesheet.id
                && _.isNumber($scope.timesheet.workHours.sunday)
                && _.isNumber($scope.timesheet.workHours.monday)
                && _.isNumber($scope.timesheet.workHours.tuesday)
                && _.isNumber($scope.timesheet.workHours.wednesday)
                && _.isNumber($scope.timesheet.workHours.thursday)
                && _.isNumber($scope.timesheet.workHours.friday)
                && _.isNumber($scope.timesheet.workHours.saturday);
        };

        $scope.allowEdit = function() {
            return $scope.timesheet
                && !$scope.timesheet.id;
        };

        // Register the confirm message for saving timesheet, so that the 
        // auto confirm directive can use this properly.
        $scope.saveTimesheetConfirmText =  'Do you want to proceed with submitting the timesheet?\n'
                            + 'Please note once submitted, no further changes are allowed on this timesheet.';
        $scope.saveTimesheet = function() {
            WorkTimesheetService.CreateWorkTimesheet($scope.timesheet)
            .then(
                function(resultTimesheet) {
                    $scope.reloadTimesheet();

                    var successMessage = "Your work hour timesheet has been submitted successfully!"
                    $scope.showMessageWithOkayOnly('Success', successMessage);
                },
                function(errors) {
                    var message = 'Failed to save the timesheet. Please try again later.';
                    $scope.showMessageWithOkayOnly('Error', message);
                }
            );
        };
    }
  ];

  return {
    restrict: 'E',
    scope: {
        user: '=',
        adminMode: '=',
        company: '='
    },
    templateUrl: '/static/partials/work_timesheet/directive_work_timesheet_manager.html',
    controller: controller
  };
});
