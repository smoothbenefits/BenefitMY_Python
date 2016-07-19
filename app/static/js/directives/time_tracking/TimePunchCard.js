BenefitMyApp.controller('TimePunchCardController', [
    '$scope',
    '$modal',
    '$attrs',
    '$controller',
    'DateTimeService',
    function TimePunchCardController(
      $scope,
      $modal,
      $attrs,
      $controller,
      DateTimeService) {

        // Inherite scope from base
        $controller('modalMessageControllerBase', {$scope: $scope});

        $scope.$watchGroup(['user', 'company'], function(watchGroup) {
          if(watchGroup && watchGroup[0] && watchGroup[1]){
            // Populate the weeks for display
            $scope.listOfWeeks = DateTimeService.GetListOfWeeks(10, 15);

            $scope.selectedDisplayWeek = _.find($scope.listOfWeeks, function(weekItem) {
                return weekItem.isCurrentWeek;
            });

            $scope.reloadTimePunchCard();
          }
        });

        $scope.reloadTimePunchCard = function() {
        };
    }
  ]
).directive('bmTimePunchCard', function() {
  return {
    restrict: 'E',
    scope: {
        user: '=',
        company: '='
    },
    templateUrl: '/static/partials/time_punch_card/directive_time_punch_card.html',
    controller: 'TimePunchCardController'
  };
});
