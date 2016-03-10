BenefitMyApp.controller('TimePunchCardEditModalController', [
  '$scope', '$modalInstance', 'user', 'week', 'WorkTimesheetService',
  function($scope, $modalInstance, user, week, WorkTimesheetService){
    $scope.week = week;
    $scope.adminMode = true;
    $scope.saveResult = function(savedTimecards){
        $modalInstance.close(savedTimecards);
    }
    $scope.dismiss = function() {
      $modalInstance.dismiss();
    };
  }
]).controller('TimePunchCardDirectiveController', [
    '$scope',
    '$modal',
    '$attrs',
    '$controller',
    'WorkTimesheetService',
    'CompanyPersonnelsService',
    function TimePunchCardDirectiveController(
      $scope,
      $modal,
      $attrs,
      $controller,
      WorkTimesheetService,
      CompanyPersonnelsService) {

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


        $scope.$watch('user', function(theUser) {
            if(theUser){
                // Populate the weeks for display
                $scope.listOfWeeks = getListOfWeeks();

                $scope.selectedDisplayWeek = _.find($scope.listOfWeeks, function(weekItem) {
                    return weekItem.isCurrentWeek;
                });
            }
        });

        $scope.saveResult = function(savedTimeSheet){
            if(savedTimeSheet){
                $state.reload();
                var successMessage = "Your timesheet has been submitted successfully!"
                $scope.showMessageWithOkayOnly('Success', successMessage);
            }
            else{
                var message = 'Failed to save the timesheet. Please try again later.';
                $scope.showMessageWithOkayOnly('Error', message);
            }
        }

        $scope.viewDetails = function(){
            var modalInstance = $modal.open({
                templateUrl: '/static/partials/work_timesheet/modal_edit_time_punch_card.html',
                controller: 'TimePunchCardEditModalController',
                size: 'lg',
                backdrop: 'static',
                resolve: {
                  'user': function() {
                    return $scope.user;
                  },
                  'week': function(){
                    return $scope.selectedDisplayWeek;
                  }
                }
              });

            modalInstance.result.then(function(savedTimesheet){
                $state.reload();
            });
        };
    }
  ]
).directive('bmTimePunchCardManager', function() {
  return {
    restrict: 'E',
    scope: {
        user: '=',
        adminMode: '=',
        company: '='
    },
    templateUrl: '/static/partials/time_punch_card/directive_time_punch_card_manager.html',
    controller: 'TimePunchCardDirectiveController'
  };
});
