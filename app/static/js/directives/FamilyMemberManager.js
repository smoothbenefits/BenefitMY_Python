BenefitMyApp.controller(
  'employeeFamilyMemberEditModalController',
  ['$scope',
   '$modalInstance',
   'PersonService',
   'person',
   'employeeId',
  function employeeFamilyMemberEditModalController(
    $scope,
    $modalInstance,
    PersonService,
    person,
    employeeId){
    $scope.person = person;
    $scope.cancel = function(){
      $modalInstance.dismiss();
    };
    $scope.save = function(){
      PersonService.savePersonInfo(employeeId, $scope.person)
      .then(function(successResponse){
        alert('Save success!');
        $modalInstance.close(successResponse);
      }, function(errorResponse){
          alert('Failed to save the user. The error is: ' + JSON.stringify(errorResponse.data) +'\n and the http status is: ' + errorResponse.status);
      });
    };
  }
])
.controller(
  'employeeFamilyMemberViewModalController',
  ['$scope',
   '$modalInstance',
   'member',
    function employeeFamilyMemberViewModalController(
      $scope,
      $modalInstance,
      member){

      $scope.member = member;

      $scope.ok = function () {
        $modalInstance.dismiss();
      };

      $scope.edit = function(){
        $modalInstance.close();
      };
  }
])
.directive('bmFamilyMemberManager', function() {

  var controller = [
    '$scope',
    '$state',
    '$modal',
    'PersonService',
    function FamilyMemberManagerDirectiveController(
      $scope,
      $state,
      $modal,
      PersonService) {

      var selfPerson = {address: {}, phone: {}};
      $scope.family=[];
      PersonService.getFamilyInfo($scope.employee)
      .then(function(family){
        _.each(family, function(member){
          if(member.relationship === 'self'){
            selfPerson = member;
          }
          else{
            $scope.family.push(member);
          }
        });
      });

      $scope.isOnboarding = $scope.onboard;
      $scope.currentRole = $scope.role;

      var openEditModal = function(member){
        var modalInstance = $modal.open({
          templateUrl: '/static/partials/family_management/edit_form.html',
          controller: 'employeeFamilyMemberEditModalController',
          size: 'lg',
          backdrop: 'true',
          resolve: {
            person: function () {
              return member;
            },
            employeeId: function(){
              return $scope.employee;
            }
          }
        });
        return modalInstance;
      };

      $scope.viewDetails = function(member){
        var modalInstance = $modal.open({
          templateUrl: '/static/partials/family_management/view_member.html',
          controller: 'employeeFamilyMemberViewModalController',
          size: 'lg',
          backdrop: 'true',
          resolve: {
            member: function () {
              return member;
            }
          }
        });
        modalInstance.result.then(function(){
          openEditModal(member);
        });
      };

      $scope.editMember = function(member){
        openEditModal(member);
      };

      $scope.addMember = function(){
        var newPerson = {person_type:'family'};
        newPerson.address = selfPerson.address;
        newPerson.phone = selfPerson.phone;
        var modalInstance = openEditModal(newPerson);
        modalInstance.result
        .then(function(successResponse){
          if(successResponse){
            $state.reload();
          }
        });
      };
    }
  ];

  return {
    restrict: 'E',
    scope: {
    	employee: '=',
      onboard: '=?',
    	editorUserId: '=?'
    },
    templateUrl: '/static/partials/family_management/directive_main.html',
    controller: controller
  };
});
