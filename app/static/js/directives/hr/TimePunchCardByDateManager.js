BenefitMyApp.controller('TimePunchCardByDateDirectiveController', [
    '$scope',
    '$modal',
    '$controller',
    'WorkTimePunchCardService',
    function TimePunchCardByDateDirectiveController(
      $scope,
      $modal,
      $controller,
      WorkTimePunchCardService) {

        // Inherite scope from base
        $controller('modalMessageControllerBase', {$scope: $scope});

        var getWeekFromDate = function(){
          var theStartDate = moment($scope.dateOfWeek).startOf('week');
          var theEndDate = moment($scope.dateOfWeek).endOf('week');
          var selectedWeek = {
              weekStartDate: theStartDate,
              weekDisplayText: theStartDate.format(SHORT_DATE_FORMAT_STRING)
                              + ' - '
                              + theEndDate.format(SHORT_DATE_FORMAT_STRING)
          };
          return selectedWeek;
        };

        var setDateOfWeek = function(dateToSet){
          $scope.dateOfWeek = dateToSet;
          $scope.selectedWeek = getWeekFromDate();
          $scope.selectedDate = 
            $scope.selectedWeek.weekStartDate.format(SHORT_DATE_FORMAT_STRING);
          $scope.reloadTimePunchCard();
        };

        $scope.init = function(){
          $scope.$watchGroup(['user', 'company'], function(watchGroup) {
            if(watchGroup && watchGroup[0] && watchGroup[1]){
              // Populate the weeks for display
              if($scope.startDate){
                setDateOfWeek(moment($scope.startDate));
              }
              else{
                setDateOfWeek(moment());
              }
            }
          });

          $scope.$watch('selectedDate', function(){
            setDateOfWeek($scope.selectedDate);
          });
        };

        $scope.reloadTimePunchCard = function() {
          if($scope.user && $scope.company){
            WorkTimePunchCardService.GetWorkPunchCardByEmployeeUser(
                $scope.user,
                $scope.company,
                $scope.selectedWeek.weekStartDate)
            .then(function(punchcard) {
              $scope.workPunchCard = punchcard;
              $scope.workHoursByStateList =
                WorkTimePunchCardService.GetWorkHoursByState($scope.workPunchCard);
            });
          }
        };

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

        $scope.init();
    }
  ]
).directive('bmTimePunchCardByDateManager', function() {
  return {
    restrict: 'E',
    scope: {
        user: '=',
        company: '=',
        startDate: '='
    },
    templateUrl: '/static/partials/time_punch_card/directive_time_punch_card_by_date.html',
    controller: 'TimePunchCardByDateDirectiveController'
  };
});
