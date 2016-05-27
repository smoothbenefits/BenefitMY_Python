BenefitMyApp.controller('TimePunchCardEditModalController', [
  '$scope', '$modalInstance', 'user', 'workPunchCard', 'WorkTimesheetService',
  function($scope, $modalInstance, user, workPunchCard, WorkTimesheetService){
    $scope.user = user;
    $scope.adminMode = true;
    $scope.workPunchCard = workPunchCard;
    $scope.saveResult = function(savedPunchCards){
        $modalInstance.close(savedPunchCards);
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
    'WorkTimePunchCardService',
    'CompanyPersonnelsService',
    'CompanyEmployeeSummaryService',
    function TimePunchCardDirectiveController(
      $scope,
      $modal,
      $attrs,
      $controller,
      WorkTimePunchCardService,
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

        $scope.reloadTimePunchCard = function() {
          WorkTimePunchCardService.GetWorkPunchCardByEmployeeUser(
              $scope.user,
              $scope.company,
              $scope.selectedDisplayWeek.weekStartDate)
          .then(function(punchcard) {
            $scope.workPunchCard = punchcard;
            $scope.workHoursByStateList =
              WorkTimePunchCardService.GetWorkHoursByState($scope.workPunchCard);
          });

          CompanyPersonnelsService.getCompanyEmployees($scope.company.id)
            .then(function(employees){
                WorkTimePunchCardService.GetWorkPunchCardsByCompany(
                    $scope.company.id,
                    $scope.selectedDisplayWeek.weekStartDate)
                .then(function(timePunchCards){
                    $scope.employeeTimeCards = [];
                    _.each(employees, function(employee){
                        var employeeTimeCard = _.find(timePunchCards, function(timeCard){
                            return timeCard.employee.email == employee.user.email
                        });
                        if (!employeeTimeCard){
                            employeeTimeCard =
                                WorkTimePunchCardService.GetBlankPunchCardForEmployeeUser(
                                    employee.user,
                                    $scope.company,
                                    $scope.selectedDisplayWeek.weekStartDate);
                        }
                        $scope.employeeTimeCards.push(employeeTimeCard);
                    });
                });
            });
        };

        $scope.hasFiledPunchCardForCurrentWeek = function() {
          return $scope.workPunchCard && $scope.workPunchCard.id;
        };

        $scope.$watch('user', function(theUser) {
          if(theUser){
            // Populate the weeks for display
            $scope.listOfWeeks = getListOfWeeks();

            $scope.selectedDisplayWeek = _.find($scope.listOfWeeks, function(weekItem) {
                return weekItem.isCurrentWeek;
            });

            $scope.reloadTimePunchCard();
          }
        });

        $scope.saveResult = function(savedPunchCards){
          if(savedPunchCards){
            $scope.reloadTimePunchCard();
            var successMessage = "Your timesheet has been submitted successfully!"
            $scope.showMessageWithOkayOnly('Success', successMessage);
          }
          else{
            var message = 'Failed to save the timesheet. Please try again later.';
            $scope.showMessageWithOkayOnly('Error', message);
          }
        };

        $scope.viewDetails = function(workPunchCard){
          var modalInstance = $modal.open({
            templateUrl: '/static/partials/time_punch_card/modal_edit_time_punch_card.html',
            controller: 'TimePunchCardEditModalController',
            size: 'lg',
            backdrop: 'static',
            resolve: {
              'user': function() {
                return $scope.user;
              },
              'workPunchCard': function(){
                return workPunchCard;
              }
            }
          });

          modalInstance.result.then(function(savedPunchCards){
              $scope.reloadTimePunchCard();
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
