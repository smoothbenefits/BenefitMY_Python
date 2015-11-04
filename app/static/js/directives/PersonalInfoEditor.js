BenefitMyApp.directive('bmPersonalInfoEditor', function() {

  var controller = [
    '$scope',
    '$state',
    '$window',
    'PersonService',
    function PersonalInfoEditorDirectiveController(
      $scope,
      $state,
      $window,
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
            alert('Changes saved successfully');
            if($scope.onboard && $scope.editorUserId){
              $state.go('employee_family', {employeeId: $scope.editorUserId, onboard:true});
            } else{
              $window.history.back();
            }
          }, function(errorResponse){
            alert('Failed to add the basic info. The error is: ' +
                  JSON.stringify(errorResponse.data) +
                  '\n and the http status is: ' + errorResponse.status);
          });
        };
    }
  ];

  return {
    restrict: 'E',
    scope: {
    	target: '=',
      onboard: '=?',
      editorUserId: '=?'
    },
    templateUrl: '/static/partials/common/directive_personal_info_edit.html',
    controller: controller
  };
});
