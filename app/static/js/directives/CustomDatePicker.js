BenefitMyApp.directive('bmDatePicker', function() {
  return {
    restrict: 'E',
    scope: {
    	model: '=',
    	required: '=',
      fieldname: '=',
    	disabled: '=?',
      dirty: '='
    },
    templateUrl: '/static/partials/common/datepicker.html',
    controller: ['$scope',
                function($scope) {
                  if ($scope.model) {
                    $scope.model = moment($scope.model).format('MM/DD/YYYY');
                  } else {
                    $scope.model = null;
                  }
                  if(!$scope.fieldname){
                    $scope.fieldname = 'date_field';
                  }
                  $scope.opened = false;
                  $scope.format = 'MM/dd/yyyy';

                  $scope.pickADate = function ($event) {
                    $event.preventDefault();
                    $event.stopPropagation();

                    $scope.opened = !$scope.opened;
                  };

                  $scope.dateValidate = function(){
                    return !$scope.model && $scope.required && $scope.dirty;
                  };
                }]
    };
  }
)
