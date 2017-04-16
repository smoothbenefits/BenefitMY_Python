BenefitMyApp.directive('bmPersonalInfoEditor', function() {

  var controller = [
    '$scope',
    '$state',
    '$window',
    '$attrs',
    'PersonService',
    function PersonalInfoEditorDirectiveController(
      $scope,
      $state,
      $window,
      $attrs,
      PersonService) {

        PersonService.getSelfPersonInfo($scope.target)
        .then(function(basicInfo) {
          $scope.person = basicInfo;
          $scope.infoAvailable = true;
        }, function(error) {
          if (!error.exists) {
            $scope.person = {};
            $scope.infoAvailable = false;
          }
        });

        $scope.updateBasicInfo = function(){
          PersonService.savePersonInfo($scope.person.user, $scope.person)
          .then(function(response){
            if($scope.onboard){
              alert('Changes saved successfully');
              $state.go('employee_family', {employeeId: $scope.target, onboard:true});
            } else if ('onSave' in $attrs && $scope.onSave){
              $scope.onSave({savedResponse: response});
            } else {
              alert('Changes saved successfully');
              $window.history.back();
            }
          }, function(errorResponse){
            alert('Failed to add the basic info. The error is: ' +
                  JSON.stringify(errorResponse.data) +
                  '\n and the http status is: ' + errorResponse.status);
          });
        };

        $scope.cancel = function(){
          if('onCancel' in $attrs && $scope.onCancel){
            $scope.onCancel();
          } else {
            $window.history.back();
          }
        };
    }
  ];

  return {
    restrict: 'E',
    scope: {
      target: '=',
      onboard: '=?',
      // Call back when successfully saved
      onSave: '&',
      // Call back when cancel is called
      onCancel: '&',
    },
    templateUrl: '/static/partials/common/directive_personal_info_edit.html',
    controller: controller
  };
});
