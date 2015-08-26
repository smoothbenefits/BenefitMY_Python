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

        if ($scope.maskssn) {
          $scope.ssnDisplayType = 'password';
        } else {
          $scope.ssnDisplayType = 'tel';
        }

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
    	target: '=',
      maskssn: '=',
      onboard: '=?',
    	editorUserId: '=?'
    },
    templateUrl: '/static/partials/common/personal_info_edit.html',
    controller: controller
  };
});
