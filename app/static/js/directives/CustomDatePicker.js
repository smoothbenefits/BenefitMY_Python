BenefitMyApp.directive('bmDatePicker', function() {
  return {
    restrict: 'E',
    scope: {
    	model: '=',
    	required: '=',
    	disabled: '=?'
    },
    templateUrl: '/static/partials/common/datepicker.html',
    controller: ['$scope',
                function($scope) {
                  if ($scope.model) {
                    $scope.model = moment($scope.model).format('MM/DD/YYYY');
                  } else {
                    $scope.model = moment().format('MM/DD/YYYY');
                  }
                  $scope.opened = false;
                  $scope.format = 'MM/dd/yyyy';

                  $scope.pickADate = function ($event) {
                    $event.preventDefault();
                    $event.stopPropagation();

                    $scope.opened = !$scope.opened;
                  };
                }]
    };
  }
)