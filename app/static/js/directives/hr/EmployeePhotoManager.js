BenefitMyApp.controller('EmployeePhotoManagerDirectiveController', [
  '$scope',
  '$state',
  '$modal',
  '$controller',
  'EmployeeProfileService',
  function($scope,
           $state,
           $modal,
           $controller,
           EmployeeProfileService){

    // Inherite scope from base
    $controller('modalMessageControllerBase', {$scope: $scope});

    // The view needs both employee and company information to generate
    // right context information for operations
    $scope.$watchGroup(['employeeUserId', 'companyId'], function(newValues) {
        var employeeUserId = newValues[0];
        var companyId = newValues[1];
        if(employeeUserId && companyId) {
            EmployeeProfileService.getEmployeeProfileForCompanyUser(companyId, employeeUserId).then(function(employeeProfile) {
                $scope.employeeProfile = employeeProfile;
            });
        }
    });

    $scope.hasPhoto = function() {
        return $scope.employeeProfile && $scope.employeeProfile.photoUrl;
    };

    $scope.deletePhoto = function() {
        $scope.employeeProfile.photoUrl = null;
        EmployeeProfileService.saveEmployeeProfile($scope.employeeProfile)
        .then(function(response){
            $scope.showMessageWithOkayOnly('Success', 'Employee Photo has been deleted successfully.'); 
        }, function(error){
            $scope.showMessageWithOkayOnly('Failed', 'Failed to delete employee photo.');
        });
    };
  }
]).directive('bmEmployeePhotoManager', function(){

    return {
        restrict: 'E',
        scope: {
            companyId: '=',
            employeeUserId: '='
        },
        templateUrl: '/static/partials/employee_record/directive_employee_photo_manager.html',
        controller: 'EmployeePhotoManagerDirectiveController'
      };
});
