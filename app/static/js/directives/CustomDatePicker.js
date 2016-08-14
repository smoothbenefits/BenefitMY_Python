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
        $scope.date = moment($scope.model).toDate();
        $scope.$watch('model', function(updatedModel){
          if(updatedModel){
            $scope.date = moment($scope.model).toDate();
          }
          else{
            $scope.date = null;
          }
        });

        $scope.$watch('date', function(updatedDate){
          if(updatedDate){
            $scope.model = moment($scope.date).format('MM/DD/YYYY');
          }
          else{
            $scope.model = '';
          }
        });
        
        if(!$scope.fieldname){
          $scope.fieldname = 'date_field';
        }
        $scope.opened = false;
        $scope.format = 'M/d/yyyy';

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
