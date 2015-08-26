BenefitMyApp.directive('bmPersonalInfoEditor', function() {

  var controller = [
    '$scope',
    '$state',
    'currentUser',
    'PersonService',
    function PersonalInfoEditorDirectiveController(
      $scope,
      $state,
      currentUser,
      PersonService) {

        PersonService.getSelfPersonInfo($scope.targetPersonUserId)
        .then(function(basicInfo) {
          $scope.person = basicInfo;
        });

        $scope.updateBasicInfo = function(){
          PersonService.savePersonInfo($scope.person.user.id, $scope.person)
          .then(function(response){
            alert('Changes saved successfully');
            if($scope.onboard){
              $state.go('employee_family', {employeeId: $scope.curUser.id, onboard:true});
            } else{
              $state.go('/');
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
    	targetPersonUserId: '=',
    	editorUserId: '=?'
    },
    templateUrl: '/static/partials/common/personal_info_edit.html',
    controller: controller
  };
});
