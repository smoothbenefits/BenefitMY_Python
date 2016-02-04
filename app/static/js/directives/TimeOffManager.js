BenefitMyApp.directive('bmTimeOffManager', function(){
    var controller = ['$scope',
        '$state',
        'TimeOffService',
        function TimeOffDirectiveController($scope,
                $state, 
                TimeOffService) {
            $scope.$watch('user', function(theUser){
                if(theUser){
                    TimeOffService.GetTimeOffsByRequestor(theUser.id)
                   .then(function(timeOffs){
                      $scope.requestedTimeOffs = timeOffs;
                   });
                }
            });
        }];
    return {
        restrict: 'E',
        scope: {
          user: '='
        },
        templateUrl: '/static/partials/common/directive_time_off_manager.html',
        controller: controller
      };
})