BenefitMyApp.directive('confirmUnsavedOnExit', ['$modal', '$state', function ($modal, $state) {
    return {

        restrict: "A",
        link: function($scope, elem, attrs) {

            var stopListen = $scope.$on('$stateChangeStart', function(event, toState, toParams, fromState, fromParams) {
                if ($scope.myForm.$dirty) {

                    $modal.open({
                      templateUrl: '/static/partials/common/modal_unsaved_change_confirm.html',
                      controller: 'confirmUnsavedOnExitModalCtrl',
                      size: 'md'
                    })
                    .result.then(
                        function() { stopListen(); $state.go(toState, toParams); }, 
                        function() { 
                            if ($scope.state_exit_cancelled) {
                                $scope.state_exit_cancelled(fromState); 
                            }
                        });

                    event.preventDefault(); 
                }
            });

        }
    };
}])
.controller('confirmUnsavedOnExitModalCtrl', ['$scope','$modalInstance', function($scope, $modalInstance){
    $scope.ok = function () {
          $modalInstance.close();
    };
    $scope.cancel = function () {
          $modalInstance.dismiss('cancel');
    };
}]);
